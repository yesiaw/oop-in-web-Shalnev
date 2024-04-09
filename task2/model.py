from __future__ import annotations
from typing import Optional, Iterable, List
import datetime


class Client:
    def __init__(
        self,
        client_id: int,
        name: str,
        credit_history_score: float
    ) -> None:
        self.client_id = client_id
        self.name = name
        self.credit_history_score = credit_history_score

    def __repr__(self) -> str:
        return (
            f"Client(client_id={self.client_id}, "
            f"name={self.name!r}, "
            f"credit_history_score={self.credit_history_score})"
        )


class CreditApplication:
    def __init__(
        self,
        application_id: int,
        client: Client,
        amount: float
    ) -> None:
        self.application_id = application_id
        self.client = client
        self.amount = amount
        self.status: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"CreditApplication(application_id={self.application_id}, "
            f"client={self.client!r}, "
            f"amount={self.amount}, "
            f"status={self.status})"
        )


class ScoringModel:
    def __init__(self, model_id: int, description: str) -> None:
        self.model_id = model_id
        self.description = description

    def evaluate(self, application: CreditApplication) -> float:
        return application.client.credit_history_score * 0.5 + 0.5 * (1 - min(application.amount, 10000) / 10000)

    def __repr__(self) -> str:
        return (
            f"ScoringModel(model_id={self.model_id}, "
            f"description={self.description})"
        )


class CreditDecisionEngine:
    def decide(self, application: CreditApplication, score: float) -> str:
        if score > 0.6:
            application.status = 'Approved'
        else:
            application.status = 'Denied'
        return application.status


def main():
    client = Client(1, "John Doe", 0.8)
    application = CreditApplication(101, client, 5000)
    model = ScoringModel(1, "Basic Scoring Model")
    engine = CreditDecisionEngine()

    score = model.evaluate(application)
    decision = engine.decide(application, score)

    print(client)
    print(application)
    print(f"Score: {score:.2f}")
    print(f"Decision: {decision}")


if __name__ == "__main__":
    main()
