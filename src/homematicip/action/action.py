import functools
from typing import List

from homematicip.action.registry import Registry
from homematicip.model.model_components import FunctionalChannel
from homematicip.model.hmip_base import HmipBaseModel


class Action:

    @staticmethod
    def allowed_types(*decorator_args):
        def decorator(func):
            Registry.register_allowed_types(func, decorator_args)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if "fc" in kwargs:
                    entity = kwargs["fc"]
                elif len(args) > 1:
                    entity = args[1]
                else:
                    raise ValueError("Can't find functional channel to check type.")

                if not isinstance(entity, HmipBaseModel):
                    raise ValueError(f"First argument must be of type HmipBaseModel, but is {type(entity)}")

                type_field = "type"

                if isinstance(entity, FunctionalChannel):
                    type_field = "functionalChannelType"

                if not hasattr(entity, type_field):
                    raise ValueError(f"Can't find attribute {type_field} in class {type(entity)}")

                found_type = getattr(entity, type_field)
                if found_type not in decorator_args:
                    raise ValueError(f"Type must be one of {decorator_args}, but found {found_type}")

                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def cli_commands(*decorator_args):
        def decorator(func):
            Registry.register_cli_commands(func, decorator_args)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def target_type(target):
        def decorator(func):
            Registry.register_target(func, target)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator