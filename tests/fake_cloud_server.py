from werkzeug.wrappers import Response, Request
import json
import hashlib


class FakeCloudServer():
    """ a fake server to act as the HMIP cloud"""

    def __init__(self):
        self.data = json.load(open("tests/json_data/home.json", encoding="UTF-8"))
        self.sgtin = '3014F711A000000BAD0C0DED'
        self.client_auth_token = hashlib.sha512(str(self.sgtin + "jiLpVitHvWnIGD1yo7MA").encode('utf-8')).hexdigest().upper()

        self.client_token_map = { '00000000-0000-0000-0000-000000000000' : '8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE' }

    def __call__(self,environ, start_response):
        request = Request(environ)
        response = Response()
        methodname = "{}{}".format(request.method.lower(), request.path.replace('/','_'))
        response.content_type = 'application/json;charset=UTF-8'
        try:
            respone=self.call_method(methodname,request,response)
        except NameError as e:
            response.status_code = 404
            response.data = json.dumps( { "errorCode" : str(e) })
        return response(environ,start_response)

    def validate_authorization(func):
        def func_wrapper(self,request : Request ,response : Response):
            if request.headers["CLIENTAUTH"] == self.client_auth_token:
                for v in self.client_token_map.values():
                    if v == request.headers["AUTHTOKEN"]:
                        return func(self,request,response)


            response.data = { "errorCode" : "INVALID_AUTHORIZATION" }
            response.status_code = 403

            return response
        return func_wrapper

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

    def post_getHost(self,request : Request ,response : Response):
        data = {
            "urlREST" : self.url,
            "urlWebSocket" : self.url, # needs to be changed
            "apiVersion" : "12"
            }
        response.data = json.dumps(data)
        return response


    def call_method(self,func_name,*args,**kwargs):
        if func_name[0] == '_':
            raise NameError('Can\'t call internal function {}'.format(func_name))
        def func_not_found(*args,**kwargs): # just in case we dont have the function
            raise NameError('Can\'t find method {}'.format(func_name))
        func = getattr(self,func_name,func_not_found) 
        return func(*args,**kwargs) # <-- this should work!





