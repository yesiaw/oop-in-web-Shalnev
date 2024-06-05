import datetime
from typing import Iterable, Any

from exceptions import InvalidSampleError
from hyperparameter import Hyperparameter
from sample.classified import ClassifiedSample
from sample.test import TestSample
from sample.train import TrainSample
from sample.unknown import UnknownSample


class TrainingSet:

    def __init__(self, name: str) -> None:
        self.name = name
        self.upload_time: datetime.datetime | None = None
        self.test_time: datetime.datetime | None = None
        self.train_samples: list[TrainSample] = []
        self.test_samples: list[TestSample] = []
        self.tuned_hyperparams: list[Hyperparameter] = []

    def load(self, data_entries: Iterable[dict[str, Any]]) -> None:
        for index, entry in enumerate(data_entries):
            try:
                if index % 5 == 0:
                    self.test_samples.append(TestSample.from_dict(entry))
                else:
                    self.train_samples.append(TrainSample.from_dict(entry))
            except InvalidSampleError as error:
                print(f"Entry {index + 1}: {error}")
        self.upload_time = datetime.datetime.now(datetime.timezone.utc)

    def test(self, hyperparameter: Hyperparameter) -> None:
        hyperparameter.test(self.test_samples)
        self.tuned_hyperparams.append(hyperparameter)
        self.test_time = datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def classify(hyperparameter: Hyperparameter, sample: UnknownSample) -> ClassifiedSample:
        prediction = hyperparameter.classify(sample)
        return ClassifiedSample(predict=prediction, **sample.dict())
