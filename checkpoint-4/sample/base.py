from enum import Enum
from typing import Any, Self

from pydantic import BaseModel, ValidationError

from exceptions import InvalidSampleError

class HomeType(int, Enum):
    TENANT = 1
    OWNER = 2
    HOMELESS = 3

class MaritalType(int, Enum):
    SINGLE = 1
    MARRIED = 2
    DIVORCED = 3

class JobType(int, Enum):
    FULL_TIME = 1
    PART_TIME = 2
    JOBLESS = 3

class BaseSample(BaseModel):
    seniority: int
    home: HomeType
    time: int
    age: int
    marital: MaritalType
    records: bool
    job: JobType
    expenses: float
    income: float
    assets: float
    debt: float
    amount: float
    price: float

    def __repr__(self) -> str:
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    __str__ = __repr__

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> Self:
        try:
            return cls(**row)
        except ValidationError as ex:
            raise InvalidSampleError(f"Invalid data for {cls.__name__}: {row}") from ex
