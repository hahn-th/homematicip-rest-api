from dataclasses import dataclass
import logging


@dataclass
class PersistentConfig:

    level: int = logging.INFO
    accesspoint_id: str = None
    auth_token: str = None
    log_file: str = ""


@dataclass
class Config(PersistentConfig):
    lookup_url: str = "https://lookup.homematic.com:48335/getHost"

    @classmethod
    def from_persistent_config(cls, persistent_config: PersistentConfig):
        return cls(level=persistent_config.level,
                   accesspoint_id=persistent_config.accesspoint_id,
                   auth_token=persistent_config.auth_token,
                   log_file=persistent_config.log_file)