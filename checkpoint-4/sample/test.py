from sample.known import KnownSample

class TestSample(KnownSample):
    predict: bool | None = None

    @property
    def is_predict_correct(self) -> bool:
        if self.predict is None:
            raise ValueError("Predicted value is not set.")
        return self.status == self.predict
