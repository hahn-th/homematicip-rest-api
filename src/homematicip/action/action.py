from homematicip.model.functional_channels import FunctionalChannel
from homematicip.model.hmip_base import HmipBaseModel


class Action:

    @staticmethod
    def allowed_types(*decorator_args):
        def decorator(func):
            def wrapper(*args, **kwargs):
                entity = args[1]
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
