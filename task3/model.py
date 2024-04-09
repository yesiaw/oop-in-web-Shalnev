from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict
import datetime


class Client:
    """Представляет клиента банка."""

    def __init__(self, client_id: int, name: str, credit_history: float) -> None:
        self.client_id = client_id
        self.name = name
        self.credit_history = credit_history  # Примерный показатель кредитной истории от 0 до 1

    def __repr__(self) -> str:
        return f"Client({self.client_id}, '{self.name}', Credit History: {self.credit_history})"


class CreditApplication:
    """Заявка на кредит от клиента."""

    def __init__(self, client: Client, amount: float) -> None:
        self.client = client
        self.amount = amount
        self.decision: Dict[str, str] = {"status": "Pending", "reason": ""}

    def __repr__(self) -> str:
        return f"CreditApplication(Client ID: {self.client.client_id}, Amount: {self.amount}, Decision: {self.decision})"


class ScoringStrategy(ABC):
    """Стратегия оценки кредитного скоринга."""

    @abstractmethod
    def calculate_score(self, application: CreditApplication) -> float:
        pass


class SimpleScoringStrategy(ScoringStrategy):
    """Простая стратегия оценки кредитного скоринга на основе кредитной истории."""

    def calculate_score(self, application: CreditApplication) -> float:
        # Базовый скоринг на основе кредитной истории клиента
        return application.client.credit_history * (1 - application.amount / 10000)


class DecisionMaker:
    """Движок принятия решений по кредитным заявкам."""

    def __init__(self, scoring_strategy: ScoringStrategy) -> None:
        self.scoring_strategy = scoring_strategy

    def make_decision(self, application: CreditApplication) -> None:
        score = self.scoring_strategy.calculate_score(application)
        if score > 0.5:
            application.decision["status"] = "Approved"
        else:
            application.decision["status"] = "Denied"
            application.decision["reason"] = "Insufficient credit score"
        print(f"Application Decision: {application.decision['status']} - {application.decision.get('reason', '')}")


client1 = Client(1, "Alice", 0.8)
application1 = CreditApplication(client1, 5000)

scoring_strategy = SimpleScoringStrategy()
decision_maker = DecisionMaker(scoring_strategy)

decision_maker.make_decision(application1)
print(application1)

# Демонстрация добавления новой стратегии оценки без изменения существующего кода
class AdvancedScoringStrategy(ScoringStrategy):
    """Более сложная стратегия оценки, учитывающая дополнительные факторы."""

    def calculate_score(self, application: CreditApplication) -> float:
        # Имитация расчета, включающего более сложную логику
        return application.client.credit_history * 0.9 - application.amount / 20000

# Применение новой стратегии
new_strategy = AdvancedScoringStrategy()
decision_maker.scoring_strategy = new_strategy
decision_maker.make_decision(application1)
print(application1)
