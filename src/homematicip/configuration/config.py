from dataclasses import dataclass, field
import logging
from typing import List


@dataclass
class PersistentConfig:

    level: int = logging.INFO
    accesspoint_id: str = None
    auth_token: str = None
    log_file: str = ""

    # Use the normal RestConnection without limiting instead of the RateLimitedRestConnection
    disable_rate_limit: bool = False
    # Max number of tokens in the bucket
    rate_limit_tokens: int = 10
    # Fill rate of the bucket. Every x second a new token
    rate_limit_fill_rate: int = 3


@dataclass
class Config(PersistentConfig):
    lookup_url: str = "https://lookup.homematic.com:48335/getHost"

    @classmethod
    def from_persistent_config(cls, persistent_config: PersistentConfig):
        return cls(level=persistent_config.level,
                   accesspoint_id=persistent_config.accesspoint_id,
                   auth_token=persistent_config.auth_token,
                   log_file=persistent_config.log_file)
