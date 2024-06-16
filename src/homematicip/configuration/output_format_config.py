from dataclasses import dataclass, field
from typing import List


@dataclass
class OutputFormatConfig:

    functional_channel_attributes: List[str] = field(default_factory=list)
    group_attributes: List[str] = field(default_factory=list)
    device_attributes: List[str] = field(default_factory=list)