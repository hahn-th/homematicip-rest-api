from homematicip.connection.connection_context import ConnectionContext
from homematicip.connection.rate_limited_rest_connection import RateLimitedRestConnection
from homematicip.connection.rest_connection import RestConnection


class ConnectionFactory:
    """factory class for creating connections"""

    @staticmethod
    def create_connection(context: ConnectionContext, use_rate_limited_connection: bool = True,
                          httpx_client_session=None) -> RestConnection:
        """creates a connection object with the given context"""
        if use_rate_limited_connection:
            return RateLimitedRestConnection(context, httpx_client_session=httpx_client_session)
        return RestConnection(context, httpx_client_session=httpx_client_session)
