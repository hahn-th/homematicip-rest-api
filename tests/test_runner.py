import pytest
from homematicip.configuration.config import PersistentConfig
from homematicip.connection.rest_connection import RestConnection, RestResult
from homematicip.events.event_types import ModelUpdateEvent
from homematicip.runner import Runner


def test_initalize_connection_context(mocker, config: PersistentConfig):
    url_result = ("https://localhost:4711", "wss://localhost:4711")
    mocked_lookup_urls = mocker.patch('homematicip.connection.rest_connection.ConnectionUrlResolver.lookup_urls')
    mocked_lookup_urls.return_value = url_result

    runner = Runner(config=config)
    context = runner._initialize_connection_context()

    assert context.accesspoint_id == config.accesspoint_id
    assert context.auth_token == config.auth_token
    assert context.client_auth_token is not None
    assert context.rest_url == url_result[0]
    assert context.websocket_url == url_result[1]


@pytest.mark.asyncio
async def test_runner_get_current_state(mocker, sample_data_complete, config, connection_context):
    mocked_rest_call = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    mocked_rest_call.return_value = RestResult(status=200, json=sample_data_complete)

    runner = Runner(config=config, _connection_context=connection_context,
                    _rest_connection=RestConnection(connection_context))
    result = await runner.async_get_current_state()

    assert result == sample_data_complete


@pytest.mark.asyncio
async def test_runner_async_run_home(mocker, sample_data_complete, config, connection_context):
    mocked_init_context = mocker.patch("homematicip.runner.Runner._initialize_connection_context")
    mocked_init_context.result = connection_context

    mocked_rest_call = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    mocked_rest_call.return_value = RestResult(status=200, json=sample_data_complete)

    mocked_listening = mocker.patch("homematicip.runner.Runner.async_listening_for_updates")
    mocked_listening.result = True

    runner = Runner(config=config, _connection_context=connection_context,
                    _rest_connection=RestConnection(connection_context))
    await runner.async_initialize_runner()

    assert runner.model is not None


def test_runner_websocket_connected_callable():
    runner = Runner()
    assert runner.websocket_connected is False

    runner._set_websocket_connected_state(True)
    assert runner.websocket_connected is True
    assert runner._websocket_connected is True


def test_runner_websocket_connected_event_is_raised(mocker):
    """Test that the HOME_CONNECTED event is raised when the websocket connection is established."""
    mock_publish = mocker.Mock()
    runner = Runner()
    runner.event_manager.publish = mock_publish
    runner._websocket_connected = False

    runner._set_websocket_connected_state(True)
    mock_publish.assert_called_with(ModelUpdateEvent.HOME_CONNECTED, True)


def test_runner_websocket_disconnected_event_is_raised(mocker):
    """Test that the HOME_DISCONNECTED event is raised when the websocket connection is lost."""
    mock_publish = mocker.Mock()
    runner = Runner()
    runner.event_manager.publish = mock_publish
    runner._websocket_connected = True

    runner._set_websocket_connected_state(False)
    mock_publish.assert_called_with(ModelUpdateEvent.HOME_DISCONNECTED, False)


def test_runner_home_is_connected_property(mocker, filled_model):
    """Test that the home_is_connected property returns the correct value."""
    runner = Runner(model=filled_model)
    current_connection_state = filled_model.home.connected

    assert runner.home_is_connected is current_connection_state

    runner.model.home.connected = not current_connection_state
    assert runner.home_is_connected is not current_connection_state
