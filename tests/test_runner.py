import pytest
from homematicip.configuration.config import PersistentConfig
from homematicip.connection.rest_connection import RestConnection, RestResult
from homematicip.runner import Runner


def test_initalize_connection_context(mocker, config: PersistentConfig):
    url_result = ("https://localhost:4711", "wss://localhost:4711")
    mocked_lookup_urls = mocker.patch('homematicip.connection.rest_connection.ConnectionUrlResolver.lookup_urls')
    mocked_lookup_urls.return_value = url_result

    runner = Runner(_config=config)
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

    runner = Runner(_config=config, _connection_context=connection_context,
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

    runner = Runner(_config=config, _connection_context=connection_context,
                    _rest_connection=RestConnection(connection_context))
    await runner.async_initialize_runner()

    assert runner.model is not None
