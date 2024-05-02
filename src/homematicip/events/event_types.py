from enum import Enum, auto


class EventType(Enum):
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
    ITEM_REMOVED = auto()
    ITEM_UPDATED = auto()
    ITEM_CREATED = auto()