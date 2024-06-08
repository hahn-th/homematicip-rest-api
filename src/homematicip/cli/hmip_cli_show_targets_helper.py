from dataclasses import dataclass, field
from typing import List

from homematicip.action.registry import Registry, ActionTarget, RegistryEntry


@dataclass
class CommandEntry:
    """Command entry for a function."""
    targets: set = field(default_factory=set)
    allowed_types: set = field(default_factory=set)


def build_commands_from_registry(
        registry: dict[str, RegistryEntry],
        filter_by_target: str = None,
        filter_by_allowed_types: List[str] = None,
        filter_by_cli_command: str = None) -> dict[str, CommandEntry]:
    """Build the commands from the registry."""
    commands: dict[str, CommandEntry] = {}
    for func_path, entry in registry.items():

        for command in entry.cli_commands:

            should_add = _should_add_command_to_result(command, filter_by_cli_command)
            if not should_add:
                continue

            if filter_by_allowed_types and not any(item in filter_by_allowed_types for item in entry.allowed_types):
                continue

            if filter_by_target and not _should_add_target_type(entry, filter_by_target):
                continue

            if command not in commands:
                commands[command] = CommandEntry()

            commands[command].targets.add(entry.target_type)
            commands[command].allowed_types.update(entry.allowed_types)

    return commands


def _should_add_command_to_result(command: str, filter_by_cli_command: str = None):
    """Check if the entry should be added to the result."""
    if filter_by_cli_command and filter_by_cli_command != command:
        return False

    return True


def _should_add_target_type(entry: RegistryEntry, filter_by_target: str = None):
    """Get the filtered target types."""
    if filter_by_target:
        return filter_by_target == entry.target_type.value

    return True


def _get_filtered_allowed_types(entry: RegistryEntry, filter_by_allowed_types: List[str] = None):
    """Get the filtered allowed types."""
    if filter_by_allowed_types:
        return [typename for typename in entry.allowed_types if typename in filter_by_allowed_types]

    return entry.allowed_types


def _should_add_to_result(entry: RegistryEntry,
                          filter_by_target: ActionTarget = None,
                          filter_by_allowed_type: str = None,
                          filter_by_cli_command: str = None):
    """Check if the entry should be added to the result."""
    if filter_by_target and filter_by_target not in entry.target_type:
        return False

    if filter_by_allowed_type and filter_by_allowed_type not in entry.allowed_types:
        return False

    if filter_by_cli_command and filter_by_cli_command not in entry.cli_commands:
        return False

    return True
