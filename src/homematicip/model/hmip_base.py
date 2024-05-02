from pydantic import BaseModel, ConfigDict


class HmipBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )