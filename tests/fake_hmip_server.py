import asyncio
import pathlib
import socket
import ssl

import aiohttp
from aiohttp import web
from aiohttp.resolver import DefaultResolver
from aiohttp.test_utils import unused_port

from homematicip.async.connection import AsyncConnection


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
            self.port = await unused_port()
        self.handler = self.app.make_handler()
        self.server = await self.loop.create_server(self.handler,
                                                    '127.0.0.1', self.port,
                                                    ssl=self.ssl_context)
        # return the base url and port which need to be resolved/mocked.
        resolver = FakeResolver({self.base_url:self.port}, loop=self.loop)
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
    get_host_response = {
        "urlREST": 'abc',
        "urlWebSocket": 'def'
    }

    def add_routes(self):
        self.app.router.add_routes(
            [web.post('/getHost', self.get_host)])

    async def get_host(self, request):
        return web.json_response(self.get_host_response)


class FakeConnectionHmip(BaseFakeHmip):
    """Test various connection issues"""

    def add_routes(self):
        self.app.router.add_routes([
            web.post('/go_404', self.go_404)
        ])

    async def go_404(self):
        return web.Response(status=404)


async def main(loop):
    fake_hmip = FakeLookupHmip(loop=loop, base_url='lookup.homematic.com',
                               port=48335)
    connector = await fake_hmip.start()

    async with aiohttp.ClientSession(connector=connector,
                                     loop=loop) as session:
        connection = AsyncConnection(loop, session)
        # async with session.get('https://lookup.homematic.com:48335/getHost',
        #                        params={'access_token': token}) as resp:
        #     print(await resp.json())
        connection.set_auth_token('auth_token')
        await connection.init('accesspoint_id')
        print(connection._urlREST)

    await fake_hmip.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
