from homematicip.model.client import Client
from homematicip.model.devices import Device
from homematicip.model.group import Group
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.model.home import Home


class Model(HmipBaseModel):
    clients: dict[str, Client] = {}
    devices: dict[str, Device] = {}
    groups: dict[str, Group] = {}
    home: Home
