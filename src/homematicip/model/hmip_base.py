from pydantic import BaseModel, ConfigDict


class HmipBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )

    def update_from_dict(self, data_dict):
        for field_name, value in data_dict.items():
            target_field = getattr(self, field_name)

            if target_field is None:
                continue

            if isinstance(target_field, HmipBaseModel):
                target_field.update_from_dict(value)

            else:
                setattr(self, field_name, value)
                #
                # if isinstance(value, dict) and issubclass(field.outer_type_, BaseModel):
                #     field_value = getattr(self, field_name, None)
                #     if isinstance(field_value, BaseModel):
                #         field_value.update_from_dict(value)
                #     else:
                #         setattr(self, field_name, field.outer_type_(**value))
                # else:
                #     setattr(self, field_name, value)