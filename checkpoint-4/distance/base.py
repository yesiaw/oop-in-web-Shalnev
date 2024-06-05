from abc import ABC, abstractmethod
from typing import Iterable, Any

from exceptions import InvalidCoefficientValue
from sample.base import BaseSample


class BaseDistance(ABC):

    @abstractmethod
    def distance(self, s1: Any, s2: Any) -> float:
        ...


class BaseSampleDistance(BaseDistance):

    @property
    @abstractmethod
    def k(self) -> int:
        ...

    @staticmethod
    @abstractmethod
    def reduction(values: Iterable[float]) -> float:
        ...

    def distance(self, s1: BaseSample, s2: BaseSample) -> float:
        if self.k == 0:
            raise InvalidCoefficientValue("Coefficient k cannot be zero.")

        attributes = ['seniority', 'home', 'time', 'age', 'marital', 'records',
                      'job', 'expenses', 'income', 'assets', 'debt', 'amount', 'price']

        values = [abs(getattr(s1, attr) - getattr(s2, attr)) ** self.k for attr in attributes]

        reduced_value = self.reduction(values)

        return float(reduced_value ** (1 / self.k))
