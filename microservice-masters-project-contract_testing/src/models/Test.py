from enum import Enum
from pydantic import BaseModel, PositiveInt, conint, constr,Json
from datetime import date, timedelta

from typing import Any, List, Optional

from models.Contract import Contract
from models.Service import Service
from models.Schema import Schema

class Result(BaseModel):
    total: conint(ge=0)
    passed: conint(ge=0)
    failed: conint(ge=0)
    duration: float
    wasSuccessful: bool
    reportPath: Optional[str] = ""


class Test(BaseModel):
    name: constr(min_length=1)
    id: constr(min_length=1)
    contracts: List[Contract]
    schemas: List[Schema]
    service: Service
    start_date: float
    results: Optional[Result] = None