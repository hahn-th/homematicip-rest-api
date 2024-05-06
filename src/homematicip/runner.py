from dataclasses import dataclass
import json
import logging

from homematicip.auth import Auth
from homematicip.configuration.config import PersistentConfig, Config
from homematicip.configuration.config_io import ConfigIO
from homematicip.connection.client_token_builder import ClientTokenBuilder
from homematicip.connection.rest_connection import (
    ClientCharacteristicsBuilder,
    ConnectionContext,
    ConnectionUrlResolver,
    RestConnection,
    WebSocketHandler,
)
from homematicip.events.event_manager import EventManager
from homematicip.events.hmip_event_handler import HmipEventHandler
from homematicip.model.model import Model
from homematicip.model import build_model_from_json

LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Runner:
    model: Model = None
    event_manager: EventManager = None

    _connection_context: ConnectionContext = None
    _rest_connection: RestConnection = None
    _config: Config = None

    def __post_init__(self):
        if self.event_manager is None:
            self.event_manager = EventManager()

    def _ensure_config(self):
        """Ensure that a configuration is set. If not, try to load it from well-known locations."""
        if self._config is None:
            config = ConfigIO.find_config_in_well_known_locations()
            if config is None:
                raise ValueError("No configuration set via set_config() and no configuration found in well-known "
                                 "locations.")
            self._config = Config.from_persistent_config(config)

        if self._config.accesspoint_id is None or self._config.auth_token is None:
            raise ValueError("Invalid configuration. Accesspoint ID and Auth Token must be set.")

    def _initialize_connection_context(self) -> ConnectionContext:
        """Initialize the connection context with the given configuration. """
        self._ensure_config()

        return ConnectionContext.create(self._config.accesspoint_id, self._config.lookup_url, self._config.auth_token)

    async def async_initialize_runner(self):
        self._connection_context = self._initialize_connection_context()
        self._rest_connection = RestConnection(self._connection_context)

        # download current configuration and build model
        current_configuration = await self.async_get_current_state()
        self.model = build_model_from_json(current_configuration)

    async def async_initialize_runner_without_init_model(self):
        """Initialize just the context and connection. Use async_get_current_state to get the current state."""
        self._connection_context = self._initialize_connection_context()
        self._rest_connection = RestConnection(self._connection_context)

    async def async_listening_for_updates(self):
        """Start listening for updates from HomematicIP Cloud. This method will not return."""
        await self._async_start_listening_for_updates(self._connection_context)

    async def async_get_current_state(self):
        """
        Ask HomematicIP Cloud for the current complete configuration and return resulting json object.
        :return: The current configuration as json object.
        """
        result = await self._rest_connection.async_post("home/getCurrentState", ClientCharacteristicsBuilder.get(
            self._connection_context.accesspoint_id))
        return result.json

    async def _async_start_listening_for_updates(self, context: ConnectionContext):
        handler = WebSocketHandler()
        hmip_event_handler = HmipEventHandler(event_manager=self.event_manager, model=self.model)
        async for message in handler.listen(context, False):
            try:
                await hmip_event_handler.process_event_async(json.loads(message))

            except Exception as e:
                LOGGER.error(f"Error while handling incoming event. Message: {message}", exc_info=e)

    @property
    def rest_connection(self):
        return self._rest_connection
