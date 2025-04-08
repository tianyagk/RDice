from pydantic import BaseModel
from enum import Enum


class Config(BaseModel):
    command_priority: int = 5
    plugin_enabled: bool = True