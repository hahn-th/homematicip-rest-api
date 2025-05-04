from unittest.mock import AsyncMock

import pytest
from websockets.exceptions import ConnectionClosedError

from homematicip.connection.connection_context import ConnectionContext
from homematicip.connection.websocket_handler import WebSocketHandler
from homematicip.exceptions.connection_exceptions import HmipConnectionError


async def test_raise_connection_closed_error():
    """Test that the connection closed error is raised."""
    # Setup
    context = ConnectionContext(
        websocket_url="wss://example.com/ws",
        auth_token="test-auth-token",
        client_auth_token="test-client-token",
        accesspoint_id="test-ap-id"
    )

    handler = WebSocketHandler()

    connection_close_error = ConnectionClosedError(rcvd=None, sent=None)
    handler._listen_internal = AsyncMock(side_effect=connection_close_error)

    with pytest.raises(HmipConnectionError) as excinfo:
        await handler.listen(context, reconnect_on_error=False)

    handler._listen_internal.assert_called_once()

    assert isinstance(excinfo.value.__cause__, ConnectionClosedError)
    assert excinfo.value.__cause__ == connection_close_error