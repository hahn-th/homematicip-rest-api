from werkzeug.wrappers import Response, Request
import json


class FakeCloudServer():
    """ a fake server to act as the HMIP cloud"""

    def __init__(self):
        self.data = json.load(open("tests/json_data/home.json", encoding="UTF-8"))

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

    def post_hmip_home_getCurrentState(self,request : Request ,response : Response):
        response.data = json.dumps(self.data)
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





