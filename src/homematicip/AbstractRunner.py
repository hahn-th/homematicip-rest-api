import abc
import asyncio
from typing import Any


class AbstractRunner(abc.ABC):
    """Abstract runner."""

    @abc.abstractmethod
    async def async_initialize_runner(self):
        """Initialize the runner with the model and the context."""
        pass

    @abc.abstractmethod
    async def async_initialize_runner_without_init_model(self):
        """Initialize just the context and connection. Use async_get_current_state to get the current state."""
        pass

    @abc.abstractmethod
    async def async_listening_for_updates(self):
        """Start listening for updates from the homematicip access point. This method will not return."""
        pass

    @abc.abstractmethod
    async def async_get_current_state(self):
        """Return the current state of the homematicip access point."""
        pass

    @property
    @abc.abstractmethod
    def rest_connection(self):
        """Return the rest connection."""
        pass
