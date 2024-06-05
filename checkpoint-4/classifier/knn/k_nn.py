from collections import Counter
from heapq import nsmallest
from classifier.knn.base import BaseKNNClassifier
from sample.base import BaseSample
from sample.train import TrainSample


class KNNClassifier(BaseKNNClassifier):
    def classify(self, sample: BaseSample) -> bool:
        distances = [(self.distance.distance(sample, train), train) for train in self.train_data]
        k_nearest = (train.status for _, train in nsmallest(self.k, distances, key=lambda x: x[0]))

        frequency = Counter(k_nearest)
        return frequency.most_common(1)[0][0]
