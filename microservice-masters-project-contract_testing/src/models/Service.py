from enum import Enum
from pydantic import BaseModel, PositiveInt, constr,Json
from typing import Any, List, Optional


class Service(BaseModel):
    url: constr(min_length=2)
    api_key: constr(min_length=1)