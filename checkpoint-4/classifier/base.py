from abc import abstractmethod, ABC

from sample.base import BaseSample
from sample.train import TrainSample

class BaseSampleClassifier(ABC):
    def __init__(self, train_data: list[TrainSample]):
        self.train_data = train_data

    @abstractmethod
    def classify(self, s: BaseSample) -> bool:
        pass
