from enum import Enum
from pydantic import BaseModel, PositiveInt, constr,Json
from typing import Any, List, Optional


class Schema(BaseModel):
    id: int
    jsonSchema: dict