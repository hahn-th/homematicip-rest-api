# dict = {
#     "TYPE_ABC": {
#         supported_action_1: {
#             Group | FunctionalChannel | Device
#             class
#         },
#         supported_actoin_2
#     }
# }
#
# ActionId = {
#     allowed_base_classes = [FunctionalChannel, Device, Group],
#     allowed_type_definitions = [
#         ASDF_GROUP,
#         XYZ_CHANNEL,
#
#
# }
#
#
from dataclasses import dataclass, field
from enum import auto, Enum


class ActionTarget(Enum):
    DEVICE = auto()
    FUNCTIONAL_CHANNEL = auto()
    HOME = auto()
    GROUP = auto()


@dataclass
class RegistryEntry:
    action_type: type
    target_type_names: list[str] = field(default_factory=list)


class Registry:
    _registry = {}

    @classmethod
    def register_class(cls, action_type):
        cls._registry[action_type] = RegistryEntry(action_type=action_type)

    @classmethod
    def register_target_type(cls, action_type, target_type_name):
        reg_entry = cls._registry[action_type]
        reg_entry.target_type_names.append(target_type_name)

#
# class RegisterAction:
#     def __init__(self, func):
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         Registry.register_class(self.func)
#         return self.func(*args, **kwargs)
#
#
# class ActionTargetType:
#     def __init__(self, func):
#         self.func = func
#
#     def __call__(self, target_type_name: str):
#         Registry.register_target_type(self.func, target_type_name)
#
#
# @RegisterAction
# @ActionTargetType("TEST_123")
# class Action:
#     pass
