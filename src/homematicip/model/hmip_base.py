from pydantic import BaseModel, ConfigDict, Field


class HmipBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )

    def update_from_dict(self, data_dict):

        model_fields = self.model_fields
        new_item = type(self).model_validate(data_dict, strict=False)

        for field_name in model_fields.keys():

            if hasattr(new_item, field_name):
                new_value = getattr(new_item, field_name)
            else:
                new_value = None

            setattr(self, field_name, new_value)



            # if isinstance(value, dict):
            #     for key_dict, value_value in value.items():
            #         if key_dict in target_field_value:
            #             target_field_value[key_dict] = value_value
            #         else:
            #             setattr(self, field_name, value)
            #
            #     # Keys durchlaufen
            #     # Key in target_field_value suchen
            #     # Wenn gefunden, dann update_from_dict(value)

            # if isinstance(target_field_value, dict[str, HmipBaseModel]):
            #     target_field_value.update_from_dict(value)
            #
            # if isinstance(target_field_value, HmipBaseModel):
            #     target_field_value.update_from_dict(value)
            #
            # else:
            #     setattr(self, field_name, value)
            #     #
            #     # if isinstance(value, dict) and issubclass(field.outer_type_, BaseModel):
            #     #     field_value = getattr(self, field_name, None)
            #     #     if isinstance(field_value, BaseModel):
            #     #         field_value.update_from_dict(value)
            #     #     else:
            #     #         setattr(self, field_name, field.outer_type_(**value))
            #     # else:
            #     #     setattr(self, field_name, value)