from enum import Enum, auto


class EventType(Enum):
    """Events thrown by the HomematicIP Cloud API. These are handled in HmipEventHandler.
    Don't use these outside of the homematicip_rest_api package."""
    CLIENT_ADDED = auto()
    CLIENT_CHANGED = auto()
    CLIENT_REMOVED = auto()
    DEVICE_ADDED = auto()
    DEVICE_CHANGED = auto()
    DEVICE_REMOVED = auto()
    GROUP_ADDED = auto()
    GROUP_CHANGED = auto()
    GROUP_REMOVED = auto()
    HOME_CHANGED = auto()
    SECURITY_JOURNAL_CHANGED = auto()


class ModelUpdateEvent(Enum):
    """Model Update Events are thrown by the HmipEventHandler when the model is updated.
    Subscribe to these Events in EventManager."""
    ITEM_REMOVED = auto()
    ITEM_UPDATED = auto()
    ITEM_CREATED = auto()
    HOME_CONNECTED = auto()
    HOME_DISCONNECTED = auto()
