# coding=utf-8
import requests
from builtins import range
import homematicip

import logging
logger = logging.getLogger(__name__)
import sys


class HomeMaticIPObject(object):
    """This class represents a generic homematic ip object to make basic requests to the access point"""
    headers = {}
    _restCallRequestCounter = 3 #the homematic ip cloud tends to time out. retry the call X times.
    _restCallTimout = 3
    def __init__(self):
        self.headers = {'content-type': 'application/json', 'accept': 'application/json', 'VERSION': '10',
                        'AUTHTOKEN': homematicip.get_auth_token(), 'CLIENTAUTH' : homematicip.get_clientauth_token()}

    def _restCall(self, path, body = None):
        result = None
        requestPath = '{}/hmip/{}'.format(homematicip.get_urlREST(), path)
        logger.trace("_restcall path({}) body({})".format(requestPath,body))
        for i in range(0,self._restCallRequestCounter):
            try:
                result = requests.post(requestPath, data=body, headers=self.headers, timeout=self._restCallTimout)
                ret = (result.json() if result.content != "" else "")
                logger.trace("_restcall result: Errorcode={} content({})".format(result.status_code, ret))
                return ret
            except requests.Timeout:
                logger.error("call to '{}' failed due Timeout".format(requestPath))
                pass
        return { "errorCode" : "TIMEOUT" }


    def from_json(self, js):
        pass

    def __repr__(self):
        return "id({}) {}".format(self.id,self.__str__())

    def __unicode__(self):
        return u'id({})'.format(self.id)

    def __str__(self):
        if sys.version_info >= (3,0):
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')