from enum import Enum
from pydantic import BaseModel, PositiveInt, constr,Json
from typing import Any, List, Optional
from models.Service import Service
from models.Schema import Schema
from models.Contract import Contract


class Configuration(BaseModel):
    service: Service
    schemas: List[Schema]
    contracts: List[Contract]
