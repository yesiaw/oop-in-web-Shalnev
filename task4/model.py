from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Union
import datetime

# Исключения
class InvalidCreditApplicationError(Exception):
    """Исключение, возникающее при невалидных данных в заявке на кредит."""
    pass

class ScoringError(Exception):
    """Исключение, возникающее при ошибке расчета скоринга."""
    pass

# Основные классы
class Client:
    """Клиент банка."""

    def __init__(self, client_id: int, name: str, credit_history_score: float) -> None:
        self.client_id = client_id
        self.name = name
        # Оценка кредитной истории должна быть в пределах 0.0 - 1.0
        if not (0.0 <= credit_history_score <= 1.0):
            raise InvalidCreditApplicationError("Credit history score must be between 0.0 and 1.0")
        self.credit_history_score = credit_history_score

    def __repr__(self) -> str:
        return f"Client(ID: {self.client_id}, Name: {self.name}, Credit History Score: {self.credit_history_score})"

class CreditApplication:
    """Заявка на кредит."""

    def __init__(self, client: Client, amount: float) -> None:
        if amount <= 0:
            raise InvalidCreditApplicationError("Credit amount must be greater than 0")
        self.client = client
        self.amount = amount
        self.decision: Optional[str] = None

    def __repr__(self) -> str:
        decision = self.decision if self.decision else "Pending"
        return f"CreditApplication(Client ID: {self.client.client_id}, Amount: {self.amount}, Decision: {decision})"

class ScoringStrategy(ABC):
    """Стратегия оценки скоринга."""

    @abstractmethod
    def calculate_score(self, application: CreditApplication) -> float:
        """Расчет скоринга для заявки."""
        pass

class SimpleScoringStrategy(ScoringStrategy):
    """Простая стратегия оценки скоринга."""

    def calculate_score(self, application: CreditApplication) -> float:
        base_score = application.client.credit_history_score * 100
        amount_penalty = application.amount / 1000
        score = base_score - amount_penalty
        if score < 0:
            raise ScoringError("Negative scoring result")
        return score

class CreditDecisionEngine:
    """Механизм принятия решений по кредитным заявкам."""

    def __init__(self, strategy: ScoringStrategy) -> None:
        self.strategy = strategy

    def make_decision(self, application: CreditApplication) -> None:
        try:
            score = self.strategy.calculate_score(application)
            application.decision = "Approved" if score > 50 else "Denied"
        except ScoringError:
            application.decision = "Denied due to scoring error"

# Пример использования
try:
    client = Client(1, "Alice Smith", 0.85)
    application = CreditApplication(client, 2000)
    scoring_strategy = SimpleScoringStrategy()
    decision_engine = CreditDecisionEngine(scoring_strategy)
    decision_engine.make_decision(application)
    print(application)
except InvalidCreditApplicationError as e:
    print(f"Application error: {e}")
