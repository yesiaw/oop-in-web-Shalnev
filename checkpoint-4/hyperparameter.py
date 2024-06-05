from classifier.base import BaseSampleClassifier
from sample.test import TestSample
from sample.unknown import UnknownSample

class Hyperparameter:
    def __init__(self, classifier: BaseSampleClassifier):
        self.classifier = classifier
        self.quality: float | None = None

    def test(self, test_samples: list[TestSample]) -> float:
        correct_predictions = 0
        for sample in test_samples:
            sample.predict = self.classify(sample)
            if sample.is_predict_correct:
                correct_predictions += 1
        self.quality = correct_predictions / len(test_samples)
        return self.quality

    def classify(self, sample: UnknownSample | TestSample) -> bool:
        return self.classifier.classify(sample)
