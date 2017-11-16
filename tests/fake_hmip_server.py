import asyncio
import pathlib
import socket
import ssl

import aiohttp
import logging
from aiohttp import web
from aiohttp.resolver import DefaultResolver
from aiohttp.test_utils import unused_port

from homematicip.async.connection import AsyncConnection
from homematicip.base.base_connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH


class FakeResolver:
    _LOCAL_HOST = {0: '127.0.0.1',
                   socket.AF_INET: '127.0.0.1',
                   socket.AF_INET6: '::1'}

    def __init__(self, fakes, *, loop):
        """fakes -- dns -> port dict"""
        self._fakes = fakes
        self._resolver = DefaultResolver(loop=loop)

    async def resolve(self, host, port=0, family=socket.AF_INET):
        fake_port = self._fakes.get(host)
        if fake_port is not None:
            return [{'hostname': host,
                     'host': self._LOCAL_HOST[family], 'port': fake_port,
                     'family': family, 'proto': 0,
                     'flags': socket.AI_NUMERICHOST}]
        else:
            return await self._resolver.resolve(host, port, family)


class BaseFakeHmip:
    def __init__(self, *, loop, base_url, port=None):
        self.loop = loop
        self.app = web.Application(loop=loop)
        self.base_url = base_url
        self.port = port
        self.handler = None
        self.server = None
        here = pathlib.Path(__file__)
        ssl_cert = here.parent / 'server.crt'
        ssl_key = here.parent / 'server.key'
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))
        self.add_routes()

    def add_routes(self):
        pass

    async def start(self):
        if self.port is None:
            self.port = unused_port()
        self.handler = self.app.make_handler()
        self.server = await self.loop.create_server(self.handler,
                                                    '127.0.0.1', self.port,
                                                    ssl=self.ssl_context)
        # return the base url and port which need to be resolved/mocked.
        resolver = FakeResolver({self.base_url: self.port}, loop=self.loop)
        connector = aiohttp.TCPConnector(loop=self.loop, resolver=resolver,
                                         verify_ssl=False)

        return connector

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        await self.app.shutdown()
        await self.handler.shutdown()
        await self.app.cleanup()


class FakeLookupHmip(BaseFakeHmip):
    host_response = {
        "urlREST": 'abc',
        "urlWebSocket": 'def'
    }

    def add_routes(self):
        self.app.router.add_routes(
            [web.post('/getHost', self.get_host)])

    async def get_host(self, request):
        return web.json_response(self.host_response)


class FakeConnectionHmip(BaseFakeHmip):
    """Test various connection issues"""
    js_response = {'response': True}


    def add_routes(self):
        self.app.router.add_routes([
            web.post('/go_404', self.go_404),
            web.post('/go_200_no_json', self.go_200_no_json),
            web.post('/go_200_json', self.go_200_json)
        ])

    async def go_404(self, request):
        return web.Response(status=404)

    async def go_200_no_json(self, request):
        return web.Response(status=200)

    async def go_200_json(self, request):
        return web.json_response(self.js_response, status=200)


class FakeWebsocketHmip(BaseFakeHmip):
    retry = 0

    def add_routes(self):
        self.app.router.add_routes([
            web.get('/', self.websocket_handler)
        ])

    async def websocket_handler(self, request):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)

        async for msg in self.ws:
            pass

        print('websocket connection closed')

        return self.ws

    async def timeout_socket_handler(self, request):
        # self.retry += 1
        # if self.retry == 4:
        #     pass
        # else:
        #     await asyncio.sleep(5)
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)

        async for msg in self.ws:
            print("messsage received")
            # if msg.type == aiohttp.WSMsgType.TEXT:
            #     if msg.data == 'close':
            #         await self.ws.close()
            #     else:
            #         await self.ws.send_str(msg.data + '/answer')
            # elif msg.type == aiohttp.WSMsgType.ERROR:
            #     print('ws connection closed with exception %s' %
            #           self.ws.exception())

        print('websocket connection closed')

        return self.ws

    async def close_connection(self):
        await self.ws.close()


async def main(loop):
    logging.basicConfig(level=logging.DEBUG)
    fake_ws = FakeWebsocketHmip(loop=loop, base_url='ws.homematic.com')
    connector = await fake_ws.start()

    async with aiohttp.ClientSession(connector=connector,
                                     loop=loop) as session:
        connection = AsyncConnection(loop, session)

        # async with session.get('https://lookup.homematic.com:48335/getHost',
        #                        params={'access_token': token}) as resp:
        #     print(await resp.json())
        connection.headers[ATTR_AUTH_TOKEN] = 'auth_token'
        connection.headers[ATTR_CLIENT_AUTH] = 'client_auth'
        connection._urlWebSocket = 'wss://ws.homematic.com/'
        # await connection._listen_for_incoming_websocket_data(
        #     lambda x: print(x))
        connection.listen_for_websocket_data(lambda x: print(x))
        # await asyncio.sleep(1)
        # await fake_ws.close_connection()
        await asyncio.sleep(600)

        await fake_ws.stop()

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
