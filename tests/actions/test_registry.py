from homematicip.action.action import Action
from homematicip.action.registry import Registry, get_fully_qualified_name, ActionTarget


@Action.allowed_types("ACCELERATION_SENSOR", "TEST_ABC")
@Action.cli_commands("test_command", "other_command")
@Action.target_type(ActionTarget.DEVICE)
def func1(runner, test, ret_val: bool):
    return ret_val


def test_register_allowed_types():
    """Test if allowed types are registered correctly"""
    func_path = get_fully_qualified_name(func1)

    reg_entries = Registry.get_registered_types()
    assert func_path in reg_entries
    assert "ACCELERATION_SENSOR" in reg_entries[func_path].allowed_types
    assert "TEST_ABC" in reg_entries[func_path].allowed_types


def test_register_cli_commands():
    """Test if cli commands are registered correctly"""
    func_path = get_fully_qualified_name(func1)

    reg_entries = Registry.get_registered_types()
    assert func_path in reg_entries
    assert "test-command" in reg_entries[func_path].cli_commands
    assert "other-command" in reg_entries[func_path].cli_commands


def test_register_target():
    """Test if target type is registered correctly"""
    func_path = get_fully_qualified_name(func1)

    reg_entries = Registry.get_registered_types()
    assert func_path in reg_entries
    assert reg_entries[func_path].target_type == ActionTarget.DEVICE


def test_all_together():
    """Test if all decorators work together"""
    func_path = get_fully_qualified_name(func1)

    reg_entries = Registry.get_registered_types()
    assert func_path in reg_entries
    assert "ACCELERATION_SENSOR" in reg_entries[func_path].allowed_types
    assert "TEST_ABC" in reg_entries[func_path].allowed_types
    assert "test-command" in reg_entries[func_path].cli_commands
    assert "other-command" in reg_entries[func_path].cli_commands
    assert reg_entries[func_path].target_type == ActionTarget.DEVICE
