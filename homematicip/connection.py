import hashlib
import json
import locale
import platform
import logging
import requests

from homematicip.base.base_connection import BaseConnection

logger = logging.getLogger(__name__)


class Connection(BaseConnection):
    def init(
        self,
        accesspoint_id,
        lookup=True,
        lookup_url="https://lookup.homematic.com:48335/getHost",
        **kwargs
    ):
        self.set_token_and_characteristics(accesspoint_id)

        if lookup:
            while True:
                try:
                    result = requests.post(
                        lookup_url, json=self.clientCharacteristics, timeout=3
                    )
                    js = json.loads(result.text)
                    self._urlREST = js["urlREST"]
                    self._urlWebSocket = js["urlWebSocket"]
                    break
                except:
                    pass
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"

    def _restCall(self, path, body=None):
        result = None
        requestPath = "{}/hmip/{}".format(self._urlREST, path)
        logger.debug("_restcall path(%s) body(%s)", requestPath, body)
        for i in range(0, self._restCallRequestCounter):
            try:
                result = requests.post(
                    requestPath,
                    data=body,
                    headers=self.headers,
                    timeout=self._restCallTimout,
                )
                ret = result.json() if len(result.content) != 0 else ""
                logger.debug(
                    "_restcall result: Errorcode=%s content(%s)",
                    result.status_code,
                    ret,
                )
                return ret
            except requests.Timeout:
                logger.error("call to '%s' failed due Timeout", requestPath)
                pass
        return {"errorCode": "TIMEOUT"}
