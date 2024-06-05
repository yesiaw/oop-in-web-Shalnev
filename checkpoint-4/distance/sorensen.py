from distance.base import BaseDistance
from sample.base import BaseSample

class SorensenDistance(BaseDistance):

    def distance(self, s1: BaseSample, s2: BaseSample) -> float:
        attributes = [
            'seniority', 'home', 'time', 'age', 'marital', 'records',
            'job', 'expenses', 'income', 'assets', 'debt', 'amount', 'price'
        ]

        differences = [abs(getattr(s1, attr) - getattr(s2, attr)) for attr in attributes]
        sums = [abs(getattr(s1, attr) + getattr(s2, attr)) for attr in attributes]

        return sum(differences) / sum(sums) if sum(sums) != 0 else 0

