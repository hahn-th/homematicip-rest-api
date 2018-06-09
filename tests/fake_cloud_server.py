from werkzeug.wrappers import Response, Request
import json
import hashlib


class FakeCloudServer():
    """ a fake server to act as the HMIP cloud"""
#region __init__ & helper functions
    def __init__(self):
        self.data = json.load(open("tests/json_data/home.json", encoding="UTF-8"))
        self.sgtin = '3014F711A000000BAD0C0DED'
        self.client_auth_token = hashlib.sha512(str(self.sgtin + "jiLpVitHvWnIGD1yo7MA").encode('utf-8')).hexdigest().upper()

        self.client_token_map = { '00000000-0000-0000-0000-000000000000' : '8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE' }

        self.pin = None

        self.client_auth_waiting = None #used in auth 

    def __call__(self,environ, start_response):
        request = Request(environ)
        response = Response()
        methodname = "{}{}".format(request.method.lower(), request.path.replace('/','_'))
        response.content_type = 'application/json;charset=UTF-8'
        try:
            response=self.call_method(methodname,request,response)
        except NameError as e:
            response.status_code = 404
            response.data = json.dumps( { "errorCode" : str(e) })
        return response(environ,start_response)

    def call_method(self,func_name,*args,**kwargs):
        if func_name[0] == '_':
            raise NameError('Can\'t call internal function {}'.format(func_name))
        def func_not_found(*args,**kwargs): # just in case we dont have the function
            raise NameError('Can\'t find method {}'.format(func_name))
        func = getattr(self,func_name,func_not_found) 
        return func(*args,**kwargs) # <-- this should work!

    def validate_authorization(func):
        def func_wrapper(self,request : Request ,response : Response):
            try:
                if request.headers["CLIENTAUTH"] == self.client_auth_token:
                    for v in self.client_token_map.values():
                        if v == request.headers["AUTHTOKEN"]:
                            return func(self,request,response)  
            except:
                pass

            return self.errorCode(response, "INVALID_AUTHORIZATION", 403)
        return func_wrapper

    def errorCode(self,response : Response, message, status_code):
        response.data = json.dumps({ "errorCode" : message })
        response.status_code = status_code
        return response
#endregion

#region home

    @validate_authorization
    def post_hmip_home_getCurrentState(self,request : Request ,response : Response):
        response.data = json.dumps(self.data)
        return response

    @validate_authorization
    def post_hmip_home_setLocation(self,request : Request ,response : Response):

        js = json.loads(request.data)

        self.data["home"]["location"]["city"] = js["city"]
        self.data["home"]["location"]["latitude"] = js["latitude"]
        self.data["home"]["location"]["longitude"] = js["longitude"]

        return response
#endregion

#region home/security
    @validate_authorization
    def post_hmip_home_security_setZonesActivation(self,request : Request ,response : Response):

        js = json.loads(request.data)
        
        external = js["zonesActivation"]["EXTERNAL"]
        internal = js["zonesActivation"]["INTERNAL"]

        for g_id in self.data["groups"]:
            g = self.data["groups"][g_id]
            if g["type"] == "SECURITY_ZONE":
                if g["label"] == "INTERNAL":
                    g["active"] = internal
                elif g["label"] == "EXTERNAL":
                    g["active"] = external

        return response
#endregion

#region rule
    @validate_authorization
    def post_hmip_rule_enableSimpleRule(self,request : Request ,response : Response):

        js = json.loads(request.data)
        try:
            rule = self.data["home"]["ruleMetaDatas"][js["ruleId"]]
            rule["active"] = js["enabled"]
            response.status_code = 200
        except:
            response = self.errorCode(response, "INVALID_RULE", 404)
        return response

    @validate_authorization
    def post_hmip_rule_setRuleLabel(self,request : Request ,response : Response):

        js = json.loads(request.data)
        try:
            rule = self.data["home"]["ruleMetaDatas"][js["ruleId"]]
            rule["label"] = js["label"]
            response.status_code = 200
        except:
            response = self.errorCode(response, "INVALID_RULE", 404)
        return response
#endregion

#region device

    @validate_authorization
    def post_hmip_device_setDeviceLabel(self,request : Request ,response : Response):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            d["label"] = js["label"]
            response.status_code = 200
        except:
            response = self.errorCode(response, "INVALID_DEVICE", 404)
        return response

    @validate_authorization
    def post_hmip_device_configuration_setRouterModuleEnabled(self,request : Request ,response : Response):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["routerModuleEnabled"] = js["routerModuleEnabled"]
            response.status_code = 200
        except:
            response = self.errorCode(response, "INVALID_DEVICE", 404)
        return response

    @validate_authorization
    def post_hmip_device_deleteDevice(self,request : Request ,response : Response):

        js = json.loads(request.data)
        try:
            self.data["devices"].pop(js["deviceId"], None)
            response.status_code = 200
        except:
            response = self.errorCode(response, "INVALID_DEVICE", 404)
        return response
#endregion

#region auth
    def post_hmip_auth_connectionRequest(self,request : Request ,response : Response):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode(response, "INVALID_AUTH_TOKEN", 403) # error responses must be validated against the real cloud
        elif self.client_auth_waiting is not None :
            response = self.errorCode(response, "AUTH_IN_PROCESS", 403)  # error responses must be validated against the real cloud
        else:
            pin = request.headers.get("PIN",None)
            if pin != self.pin:
                response = self.errorCode(response, "INVALID_PIN", 403) # error responses must be validated against the real cloud
            else:
                js = json.loads(request.data)
                self.client_auth_waiting = js
                response.status_code = 200
        return response

    def post_hmip_auth_isRequestAcknowledged(self,request : Request ,response : Response):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode(response, "INVALID_AUTH_TOKEN", 403) # error responses must be validated against the real cloud
        else:
            js = json.loads(request.data)
            c_id = js["deviceId"]
            for c in self.data["clients"]:
                if c["id"] == c_id:
                    response = self.errorCode(response,"",200)
                    return response
        response = self.errorCode(response,"INVALID_AUTH_CHALLANGE",403)
        return response

    def post_hmip_auth_simulateBlueButton(self,request : Request ,response : Response):
        return response
#endregion


    def post_getHost(self,request : Request ,response : Response):
        data = {
            "urlREST" : self.url,
            "urlWebSocket" : self.url, # needs to be changed
            "apiVersion" : "12"
            }
        response.data = json.dumps(data)
        return response





