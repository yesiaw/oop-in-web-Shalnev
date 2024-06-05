from typing import Iterable

from distance.base import BaseSampleDistance


class ManhattanDistance(BaseSampleDistance):
    k = 1

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return sum(values)
