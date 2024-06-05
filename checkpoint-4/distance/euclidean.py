from typing import Iterable

from distance.base import BaseSampleDistance


class EuclideanDistance(BaseSampleDistance):
    k = 2

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return sum(values)
