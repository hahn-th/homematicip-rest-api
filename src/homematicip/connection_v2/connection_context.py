from dataclasses import dataclass

from homematicip.connection_v2.client_characteristics_builder import ClientCharacteristicsBuilder
from homematicip.connection_v2.client_token_builder import ClientTokenBuilder
from homematicip.connection_v2.connection_url_resolver import ConnectionUrlResolver


class ConnectionContextBuilder:

    @classmethod
    def build_context(cls, accesspoint_id: str,
                      lookup_url: str = "https://lookup.homematic.com:48335/getHost",
                      auth_token: str = None,
                      enforce_ssl: bool = True,
                      ssl_ctx=None):
        """
        Create a new connection_v2 context and lookup urls

        :param accesspoint_id: Access point id
        :param lookup_url: Url to lookup the connection_v2 urls
        :param auth_token: The Auth Token if exists. If no one is provided None will be used
        :param enforce_ssl: Disable ssl verification by setting enforce_ssl to False
        :param ssl_ctx: ssl context to use
        :return: a new ConnectionContext
        """
        ctx = ConnectionContext()
        ctx.accesspoint_id = accesspoint_id
        ctx.client_auth_token = ClientTokenBuilder.build_client_token(accesspoint_id)
        ctx.ssl_ctx = ssl_ctx
        ctx.enforce_ssl = enforce_ssl

        cc = ClientCharacteristicsBuilder.get(accesspoint_id)
        ctx.rest_url, ctx.websocket_url = ConnectionUrlResolver().lookup_urls(cc, lookup_url, enforce_ssl, ssl_ctx)

        if auth_token is not None:
            ctx.auth_token = auth_token

        return ctx


@dataclass
class ConnectionContext:
    auth_token: str = None
    client_auth_token: str = None

    websocket_url: str = "ws://localhost:8765"
    rest_url: str = None
    accesspoint_id: str = None

    enforce_ssl: bool = True
    ssl_ctx = None

    @classmethod
    def create(cls, access_point_id: str,
               lookup_url: str = "https://lookup.homematic.com:48335/getHost",
               auth_token: str = None,
               enforce_ssl: bool = True,
               ssl_ctx=None):
        """
        Create a new connection_v2 context.

        :param access_point_id: Access point id
        :param lookup_url: Url to lookup the connection_v2 urls
        :param auth_token: The Auth Token if exists. If no one is provided None will be used
        :param enforce_ssl: Disable ssl verification by setting enforce_ssl to False
        :param ssl_ctx: ssl context to use
        :return: a new ConnectionContext
        """
        ctx = ConnectionContext()
        ctx.accesspoint_id = access_point_id
        ctx.client_auth_token = ClientTokenBuilder.build_client_token(access_point_id)
        ctx.ssl_ctx = ssl_ctx
        ctx.enforce_ssl = enforce_ssl

        cc = ClientCharacteristicsBuilder.get(access_point_id)
        ctx.rest_url, ctx.websocket_url = ConnectionUrlResolver().lookup_urls(cc, lookup_url, enforce_ssl, ssl_ctx)

        if auth_token is not None:
            ctx.auth_token = auth_token

        return ctx
