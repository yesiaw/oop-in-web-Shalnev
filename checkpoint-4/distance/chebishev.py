from typing import Iterable

from distance.base import BaseSampleDistance

class ChebyshevDistance(BaseSampleDistance):

    k = 1

    @staticmethod
    def reduction(values: Iterable[float]) -> float:
        return max(values)
