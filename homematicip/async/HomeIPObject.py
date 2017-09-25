import asyncio
import logging

from .connection import Connection

logger = logging.getLogger(__name__)


class HomeMaticIPobject:
    """This class represents a generic ASYNC homematic ip object

     Makes basic requests to the access point"""
    headers = {}
    _restCallRequestCounter = 3  # the homematic ip cloud tends to time out. retry the call X times.
    _restCallTimout = 3

    def __init__(self, connection: Connection):
        self.headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'VERSION': '10',
                        'AUTHTOKEN': connection.auth_token,
                        'CLIENTAUTH': connection.clientauth_token}

        self._connection = connection
        self._websession = connection.websession


    @asyncio.coroutine
    def _restCall(self, path, body=None):
        result = None
        requestPath = '{}/hmip/{}'.format(self._connection.urlREST, path)
        logger.debug("_restcall path({}) body({})".format(requestPath, body))
        for i in range(0, self._restCallRequestCounter):
            try:
                result = yield from self._websession.post(
                    requestPath,
                    data=body,
                    headers=self.headers,
                    timeout=self._restCallTimout)
                if result.status == 200:
                    yield from result.read()
                    if result._content:
                        ret = yield from result.json()
                    else:
                        ret = True
                else:
                    ret = False
                    # Need to set content_type otherwise I get an error.
                    # 'Attempt to decode JSON with unexpected mimetype:

                # ret = (
                #     await result.json() if result.content != "" else "")
                logger.debug(
                    "_restcall result: Errorcode={} content({})".format(
                        result.status, ret))
                return ret
            except asyncio.TimeoutError:
                logger.error(
                    "call to '{}' failed due Timeout".format(requestPath))
                pass
            except Exception as e:
                logger.exception(e)
                return

            finally:
                if result is not None:
                    yield from result.release()

        return {"errorCode": "TIMEOUT"}

    def from_json(self, js):
        pass

    def __repr__(self):
        return "id({}) {}".format(self.id, self.__str__())

    def __str__(self):
        return u'id({})'.format(self.id)

        # def __str__(self):
        #     if sys.version_info >= (3, 0):
        #         return self.__unicode__()
        #     else:
        #         return unicode(self).encode('utf-8')
