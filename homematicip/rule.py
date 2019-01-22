from homematicip import HomeMaticIPObject
import json


class Rule(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents the automation rule """

    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.label = ""
        self.active = False
        self.ruleErrorCategories = []
        self.ruleType = ""
        # these 3 fill be filled from subclasses
        self.errorRuleTriggerItems = []
        self.errorRuleConditionItems = []
        self.errorRuleActionItems = []

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.active = js["active"]
        self.ruleType = js["type"]

        self.devices = []
        for errorCategory in js["ruleErrorCategories"]:
            pass  # at the moment this was always empty

    def set_label(self, label):
        """ sets the label of the rule """
        data = {"ruleId": self.id, "label": label}
        return self._restCall("rule/setRuleLabel", json.dumps(data))

    def __str__(self):
        return "{} {} active({})".format(self.ruleType, self.label, self.active)


class SimpleRule(Rule):
    """ This class represents a "Simple" automation rule """

    def enable(self):
        """ enables the rule """
        return self.set_rule_enabled_state(True)

    def disable(self):
        """ disables the rule """
        return self.set_rule_enabled_state(False)

    def set_rule_enabled_state(self, enabled):
        """ enables/disables this rule"""
        data = {"ruleId": self.id, "enabled": enabled}
        return self._restCall("rule/enableSimpleRule", json.dumps(data))

    def from_json(self, js):
        super().from_json(js)
        # self.get_simple_rule()

    def get_simple_rule(self):
        data = {"ruleId": self.id}
        js = self._restCall("rule/getSimpleRule", json.dumps(data))

        for errorRuleTriggerItem in js["errorRuleTriggerItems"]:
            pass  # at the moment this was always empty

        for errorRuleConditionItem in js["errorRuleConditionItems"]:
            pass  # at the moment this was always empty

        for errorRuleActionItem in js["errorRuleActionItems"]:
            pass  # at the moment this was always empty

        sr = js["simpleRule"]
