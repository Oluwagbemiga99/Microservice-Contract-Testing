from enum import Enum
from functools import lru_cache
from typing import Any

import yaml
from pydantic import BaseSettings, Field, constr


class LogLevels(str, Enum):
    """Enum of permitted log levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"

class ServerSettings(BaseSettings):
    """Settings for uvicorn server"""

    host: str
    port: int = Field(ge=0, le=65535)
    log_level: LogLevels
    reload: bool
    api_key: constr(min_length=1)


class Settings(BaseSettings):
    server: ServerSettings


def load_from_yaml() -> Any:
    with open("settings.yaml") as fp:
        config = yaml.safe_load(fp)
    return config


@lru_cache()
def get_settings() -> Settings:
    yaml_config = load_from_yaml()
    settings = Settings(**yaml_config)
    # print(settings.server)
    return settings
