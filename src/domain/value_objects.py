from decimal import Decimal
from dataclasses import dataclass

from .exceptions import InvariantViolation, CurrencyMismatch


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            raise InvariantViolation("Money amount must be a Decimal.")

        if self.amount < Decimal("0"):
            raise InvariantViolation("Money amount cannot be negative.")

        if not isinstance(self.currency, str) or not self.currency:
            raise InvariantViolation("Currency must be a non-empty string.")

        object.__setattr__(self, "currency", self.currency.upper())

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise CurrencyMismatch("Cannot add Money with different currencies.")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise CurrencyMismatch("Cannot subtract Money with different currencies.")
        result = self.amount - other.amount
        if result < Decimal("0"):
            raise InvariantViolation("Resulting Money cannot be negative.")
        return Money(result, self.currency)
