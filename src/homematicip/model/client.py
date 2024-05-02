from homematicip.model.hmip_base import HmipBaseModel


class Client(HmipBaseModel):
    homeId: str = ""
    id: str = ""
    label: str = ""
    clientType: str = ""