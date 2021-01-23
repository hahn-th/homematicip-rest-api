import json

from homematicip.base.enums import *
from homematicip.rule import (
    Rule,
    SimpleRule,
)


class AsyncRule(Rule):
    """ Async implementation of a homematic ip rule """

    async def set_label(self, label):
        return await self._connection.api_call(*super().set_label(label))


class AsyncSimpleRule(SimpleRule, AsyncRule):
    """ Async implementation of a homematic ip simple rule """

    async def enable(self):
        return await self.set_rule_enabled_state(True)

    async def disable(self):
        return await self.set_rule_enabled_state(False)

    async def set_rule_enabled_state(self, enabled):
        return await self._connection.api_call(*super().set_rule_enabled_state(enabled))

    async def get_simple_rule(self):
        return await self._connection.api_call(*super().get_simple_rule())
