import logging
from dataclasses import dataclass, field
from enum import auto, Enum

_LOGGER = logging.getLogger(__name__)


class ActionTarget(Enum):
    """Definition of possible targets for an action."""
    DEVICE = 'DEVICE'
    FUNCTIONAL_CHANNEL = 'FUNCTIONAL_CHANNEL'
    HOME = 'HOME'
    GROUP = 'GROUP'
    NONE = 'NONE'


def get_fully_qualified_name(func):
    """Return the fully qualified name of a function."""
    return f"{func.__module__}.{func.__name__}"


@dataclass
class RegistryEntry:
    """Registry entry for a function."""
    allowed_types: list[str] = field(default_factory=list)
    cli_commands: list[str] = field(default_factory=list)
    target_type: ActionTarget = ActionTarget.NONE


class Registry:
    """Registry for allowed types and cli commands."""
    _registry = {}

    _dict_registry: dict[str, RegistryEntry] = {}

    @classmethod
    def get_registered_types(cls) -> dict[str, RegistryEntry]:
        """Return the registered types.

        :return: dict[str, RegistryEntry] -- The registered types.
        """
        return cls._dict_registry

    @classmethod
    def register_allowed_types(cls, func, allowed_types):
        """Register allowed types for a function."""
        func_path = get_fully_qualified_name(func)
        entry = cls._get_registry_entry(func_path)
        entry.allowed_types.extend(allowed_types)

    @classmethod
    def register_cli_commands(cls, func, cli_commands):
        """Register cli commands for a function."""
        func_path = get_fully_qualified_name(func)
        commands_without_underscore = [command.replace("_", "-") for command in cli_commands]

        func_path = get_fully_qualified_name(func)
        entry = cls._get_registry_entry(func_path)
        entry.cli_commands.extend(commands_without_underscore)

    @classmethod
    def register_target(cls, func, target_type):
        """Register the target type for a function."""
        func_path = get_fully_qualified_name(func)
        entry = cls._get_registry_entry(func_path)
        entry.target_type = target_type


    @classmethod
    def _get_registry_entry(cls, func_path) -> RegistryEntry:
        """Return the registry entry for a function."""
        if func_path not in cls._dict_registry:
            cls._dict_registry[func_path] = RegistryEntry()
        return cls._dict_registry[func_path]

    @classmethod
    def clear_registry(cls):
        """Clear the registry."""
        cls._dict_registry = {}