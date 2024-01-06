import asyncio
import logging
import pathlib
import socket
import ssl

import aiohttp
from aiohttp import web
from aiohttp.resolver import DefaultResolver
from aiohttp.test_utils import unused_port

from homematicip.aio.connection import AsyncConnection
from homematicip.base.base_connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH


class FakeResolver:
    _LOCAL_HOST = {0: "127.0.0.1", socket.AF_INET: "127.0.0.1", socket.AF_INET6: "::1"}

    def __init__(self, fakes, *, loop):
        """fakes -- dns -> port dict"""
        self._fakes = fakes
        self._resolver = DefaultResolver(loop=loop)

    async def resolve(self, host, port=0, family=socket.AF_INET):
        fake_port = self._fakes.get(host)
        if fake_port is not None:
            return [
                {
                    "hostname": host,
                    "host": self._LOCAL_HOST[family],
                    "port": fake_port,
                    "family": family,
                    "proto": 0,
                    "flags": socket.AI_NUMERICHOST,
                }
            ]
        else:
            return await self._resolver.resolve(host, port, family)


class FakeServer:
    def __init__(self, loop, base_url=None, port=None):
        self.loop = loop
        self.app = web.Application(loop=loop)
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = "http://127.0.0.1:8080"
        self.add_routes()

    def add_routes(self):
        self.app.router.add_get("/", self.websocket_handler)

    async def websocket_handler(self, request):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)
        async for msg in self.ws:
            await asyncio.sleep(2)

        return self.ws

    async def start_server(self):
        self.loop.create_task(self.app.startup())


class BaseFakeHmip:
    def __init__(self, *, loop, base_url, port=None):
        self.loop = loop
        self.app = web.Application(loop=loop)
        self.base_url = base_url
        self.port = port
        self.handler = None
        self.server = None
        here = pathlib.Path(__file__)
        ssl_cert = here.parent / "server.crt"
        ssl_key = here.parent / "server.key"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))
        self.add_routes()

    def add_routes(self):
        pass

    async def start(self):
        if self.port is None:
            self.port = unused_port()
        self.handler = self.app.make_handler()
        self.server = await self.loop.create_server(
            self.handler, "127.0.0.1", self.port, ssl=self.ssl_context
        )
        # return the base url and port which need to be resolved/mocked.
        resolver = FakeResolver({self.base_url: self.port}, loop=self.loop)
        connector = aiohttp.TCPConnector(
            loop=self.loop, resolver=resolver, verify_ssl=False
        )

        return connector

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        await self.app.shutdown()
        await self.handler.shutdown()
        await self.app.cleanup()


class FakeLookupHmip(BaseFakeHmip):
    host_response = {"urlREST": "abc", "urlWebSocket": "def"}

    def add_routes(self):
        self.app.router.add_routes([web.post("/getHost", self.get_host)])

    async def get_host(self, request):
        return web.json_response(self.host_response)


class FakeConnectionHmip(BaseFakeHmip):
    """Test various connection issues"""

    js_response = {"response": True}

    def add_routes(self):
        self.app.router.add_routes(
            [
                web.post("/go_404", self.go_404),
                web.post("/go_200_no_json", self.go_200_no_json),
                web.post("/go_200_json", self.go_200_json),
            ]
        )

    async def go_404(self, request):
        return web.Response(status=404)

    async def go_200_no_json(self, request):
        return web.Response(status=200)

    async def go_200_json(self, request):
        return web.json_response(self.js_response, status=200)


class FakeWebsocketHmip(BaseFakeHmip):
    retry = 0

    def __init__(self, loop, base_url, port=None):
        super().__init__(loop=loop, base_url=base_url, port=port)
        self.connections = []

    def add_routes(self):
        self.app.router.add_routes(
            [
                web.get("/", self.websocket_handler),
                web.get("/nopong", self.no_pong_handler),
                web.get("/servershutdown", self.server_shutdown),
                web.get("/clientclose", self.client_shutdown),
                web.get("/recover", self.recover_handler),
            ]
        )

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        self.connections.append(ws)
        await ws.prepare(request)
        ws.send_bytes(b"abc")
        await asyncio.sleep(2)
        print("websocket connection closed")

        return ws

    async def recover_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        ws.send_bytes(b"abc")

        await asyncio.sleep(2)

        ws.send_bytes(b"resumed")

    async def no_pong_handler(self, request):
        ws = web.WebSocketResponse(autoping=False)
        self.connections.append(ws)
        await ws.prepare(request)
        await asyncio.sleep(20)
        return ws

    async def server_shutdown(self, request):
        ws = web.WebSocketResponse()
        self.connections.append(ws)
        await ws.prepare(request)
        self.loop.create_task(self.stop())
        await asyncio.sleep(10)
        # await self.stop()
        return ws

    async def client_shutdown(self, request):
        ws = web.WebSocketResponse()
        self.connections.append(ws)
        await ws.prepare(request)
        await asyncio.sleep(10)

    async def stop(self):
        # for _ws in self.connections:
        #     await _ws.close()
        await super().stop()


async def main(loop):
    logging.basicConfig(level=logging.DEBUG)
    fake_ws = FakeWebsocketHmip(loop=loop, base_url="ws.homematic.com")
    connector = await fake_ws.start()

    incoming = {}

    def parser(*args, **kwargs):
        incoming["test"] = None

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:
        connection = AsyncConnection(loop, session)

        connection.headers[ATTR_AUTH_TOKEN] = "auth_token"
        connection.headers[ATTR_CLIENT_AUTH] = "client_auth"
        connection._urlWebSocket = "wss://ws.homematic.com/"
        try:
            ws_loop = await connection.ws_connect(parser)
            await ws_loop
        except Exception as err:
            pass
        print(incoming)

        await fake_ws.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
