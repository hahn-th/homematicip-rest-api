import requests
import homematicip

class HomeMaticIPObject(object):
  """description of class"""
  headers = {}
  def __init__(self):
    self.headers = {'content-type':'application/json', 'accept':'application/json' , 'VERSION' : '7', 'AUTHTOKEN':homematicip.get_auth_token()}
  def _restCall(self, path, body):
    return requests.post('{}/hmip/{}'.format(homematicip.get_urlREST(),path), data=body, headers=self.headers).text
  def from_json(self,js):
    pass


