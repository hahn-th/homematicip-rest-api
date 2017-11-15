from homematicip.async.device import AsyncPlugableSwitch, \
    AsyncPlugableSwitchMeasuring
from homematicip.base.constants import PLUGABLE_SWITCH_MEASURING, \
    PLUGABLE_SWITCH

TYPE_CLASS_MAP = {
    PLUGABLE_SWITCH_MEASURING: AsyncPlugableSwitchMeasuring,
    PLUGABLE_SWITCH: AsyncPlugableSwitch,
}

TYPE_GROUP_MAP = {

}

TYPE_SECURITY_EVENT_MAP = {

}
