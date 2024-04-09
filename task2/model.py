from __future__ import annotations
from typing import Optional, Iterable
import datetime
import random


class Client:
    def __init__(self, client_id: int, name: str, credit_history: str) -> None:
        self.client_id = client_id
        self.name = name
        self.credit_history = credit_history

    def __repr__(self) -> str:
        return (
            f"Client(client_id={self.client_id}, "
            f"name={self.name!r}, "
            f"credit_history={self.credit_history!r})"
        )


class CreditApplication:
    def __init__(self, application_id: int, client_id: int, amount: float, status: Optional[str] = None) -> None:
        self.application_id = application_id
        self.client_id = client_id
        self.amount = amount
        self.status = status

    def __repr__(self) -> str:
        return (
            f"CreditApplication(application_id={self.application_id}, "
            f"client_id={self.client_id}, "
            f"amount={self.amount}, "
            f"status={self.status!r})"
        )


class CreditScoringModel:
    def __init__(self, model_id: int, model_type: str) -> None:
        self.model_id = model_id
        self.model_type = model_type

    def evaluate(self, application: CreditApplication) -> float:
        score = 0.5
        if application.amount < 5000:
            score += 0.2
        if application.amount > 15000:
            score -= 0.2
        return score


class CreditDecisionEngine:
    def make_decision(self, application: CreditApplication, score: float) -> str:
        if score > 0.6:
            application.status = "Approved"
        else:
            application.status = "Denied"
        return application.status


client = Client(1, "John Doe", "Good")
application = CreditApplication(1, client.client_id, 10000)
model = CreditScoringModel(1, "Basic")

score = model.evaluate(application)
decision = CreditDecisionEngine().make_decision(application, score)

print(client)
print(application)
print(f"Decision: {decision}")
