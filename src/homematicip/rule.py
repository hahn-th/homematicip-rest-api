import json

from homematicip.base.homematicip_object import HomeMaticIPObject


class Rule(HomeMaticIPObject):
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
        return self._run_non_async(self.set_label_async, label)

    async def set_label_async(self, label):
        """ sets the label of the rule """
        data = {"ruleId": self.id, "label": label}
        return await self._rest_call_async("rule/setRuleLabel", data)

    def __str__(self):
        return "{} {} active({})".format(self.ruleType, self.label, self.active)


class SimpleRule(Rule):
    """ This class represents a "Simple" automation rule """

    def enable(self):
        """ enables the rule """
        return self.set_rule_enabled_state(True)

    async def enable_async(self):
        """ enables the rule """
        return await self.set_rule_enabled_state(True)

    def disable(self):
        """ disables the rule """
        return self.set_rule_enabled_state(False)

    async def disable_async(self):
        """ disables the rule """
        return await self.set_rule_enabled_state(False)

    def set_rule_enabled_state(self, enabled):
        """ enables/disables this rule"""
        return self._run_non_async(self.set_rule_enabled_state_async, enabled)

    async def set_rule_enabled_state_async(self, enabled):
        """ enables/disables this rule"""
        data = {"ruleId": self.id, "enabled": enabled}
        return await self._rest_call_async("rule/enableSimpleRule", data)

    def from_json(self, js):
        super().from_json(js)
        # self.get_simple_rule()

    def get_simple_rule(self):
        return self._run_non_async(self.get_simple_rule_async)

    async def get_simple_rule_async(self):
        data = {"ruleId": self.id}
        result = await self._rest_call_async("rule/getSimpleRule", data)
        js = result.json
        for errorRuleTriggerItem in js["errorRuleTriggerItems"]:
            pass
