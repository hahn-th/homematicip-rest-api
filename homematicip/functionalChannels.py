from homematicip.group import Group

from typing import Iterable

class FunctionalChanel():
    """ this is the base class for the functional channels """

    def __init__(self):
        self.index = -1
        self.groupIndex = -1
        self.label = ""
        self.groupIndex = -1

        self.groups = Iterable[Group]

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        self.index = js["index"]
        self.groupIndex = js["groupIndex"]
        self.label = js["label"]

        self.groups = []
        for id in js["groups"]:
            for g in groups:
                if g.id == id:
                    self.groups.append(g)
                    break
