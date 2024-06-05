from abc import abstractmethod
from typing import List

from classifier.base import BaseSampleClassifier
from distance.base import BaseDistance
from sample.base import BaseSample
from sample.train import TrainSample


class BaseKNNClassifier(BaseSampleClassifier):
    def __init__(self, k: int, distance: BaseDistance, train_data: List[TrainSample]):
        self.k = k
        self.distance = distance
        super().__init__(train_data=train_data)

    @abstractmethod
    def classify(self, s: BaseSample) -> bool:
        pass
