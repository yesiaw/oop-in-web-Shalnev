import random
import pytest

from classifier.knn.k_nn import KNNClassifier
from classifier.knn.k_nn_q import KNNQClassifier
from distance.chebishev import ChebishevDistance
from distance.euclidean import EuclideanDistance
from distance.manhattan import ManhattanDistance
from distance.sorensen import SorensenDistance
from exceptions import InvalidSampleError
from hyperparameter import Hyperparameter
from sample.base import BaseSample, MaritalType, HomeType, JobType
from sample.classified import ClassifiedSample
from sample.known import KnownSample
from sample.test import TestSample
from sample.train import TrainSample
from sample.unknown import UnknownSample
from training_set import TrainingSet

random.seed(0)

TEST_SAMPLES = [
    {
        "seniority": random.randint(0, 30),
        "home": random.choice(list(HomeType)),
        "time": random.randint(1, 30 * 12),
        "age": random.randint(18, 90),
        "marital": random.choice(list(MaritalType)),
        "records": random.choice([True, False]),
        "job": random.choice(list(JobType)),
        "expenses": random.randint(0, 9999999),
        "income": random.randint(0, 9999999),
        "assets": random.randint(0, 99999999),
        "debt": random.randint(0, 999999),
        "amount": random.randint(0, 999999),
        "price": random.randint(0, 999999),
    } for _ in range(100)
]

def test_distances():
    base_sample = BaseSample.from_dict(TEST_SAMPLES[0])
    for DistanceClass in [ChebishevDistance, EuclideanDistance, ManhattanDistance, SorensenDistance]:
        assert DistanceClass().distance(base_sample, base_sample) == 0.0

    modified_sample = BaseSample.from_dict({**TEST_SAMPLES[0], "age": 20})
    for DistanceClass in [ChebishevDistance, EuclideanDistance, ManhattanDistance, SorensenDistance]:
        assert DistanceClass().distance(base_sample, modified_sample) != 0.0

def test_samples():
    base_sample = BaseSample.from_dict(TEST_SAMPLES[0])
    print(base_sample)
    unknown_sample = UnknownSample.from_dict(TEST_SAMPLES[0])
    print(unknown_sample)
    known_sample = KnownSample.from_dict({**TEST_SAMPLES[0], "status": True})
    print(known_sample)
    classified_sample = ClassifiedSample.from_dict({**unknown_sample.dict(), "predict": True})
    print(classified_sample)
    train_sample = TrainSample.from_dict({**TEST_SAMPLES[0], "status": True})
    print(train_sample)
    test_sample = TestSample.from_dict({**TEST_SAMPLES[0], "predict": True, "status": True})
    assert test_sample.is_predict_correct is True

    with pytest.raises(AttributeError):
        test_sample_without_predict = TestSample.from_dict({**TEST_SAMPLES[0], "status": True})
        print(test_sample_without_predict.is_predict_correct)

def test_training_set():
    training_set = TrainingSet(name="train")
    training_set.load(raw_rows=[{**sample, "status": random.choice([True, False])} for sample in TEST_SAMPLES])

    for ClassifierClass in [KNNClassifier, KNNQClassifier]:
        for DistanceClass in [ChebishevDistance, EuclideanDistance, ManhattanDistance, SorensenDistance]:
            for k in range(1, 10):
                classifier = ClassifierClass(k=k, distance=DistanceClass(), train_data=training_set.training)
                hyperparameter = Hyperparameter(classifier=classifier)
                training_set.test(hyperparameter)
                print(f"{k=}; {DistanceClass.__name__=}; {ClassifierClass.__name__=}; {hyperparameter.quality=}")

                random_sample = UnknownSample.from_dict(random.choice(TEST_SAMPLES))
                print(f"Random classify: {training_set.classify(hyperparameter, random_sample)}")

    with pytest.raises(InvalidSampleError):
        UnknownSample.from_dict({**random.choice(TEST_SAMPLES), "age": "bla-bla"})

def main():
    test_samples()
    test_distances()
    test
