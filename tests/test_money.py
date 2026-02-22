import pytest
from decimal import Decimal

from domain.value_objects import Money
from domain.exceptions import InvariantViolation, CurrencyMismatch


def test_money_accepts_valid_decimal():
    m = Money(Decimal("100.00"), "eur")
    assert m.amount == Decimal("100.00")
    assert m.currency == "EUR"


def test_money_rejects_float():
    with pytest.raises(InvariantViolation):
        Money(100.00, "EUR")


def test_money_rejects_negative():
    with pytest.raises(InvariantViolation):
        Money(Decimal("-1.00"), "EUR")


def test_money_allows_zero():
    m = Money(Decimal("0.00"), "EUR")
    assert m.amount == Decimal("0.00")


def test_money_add_same_currency():
    m1 = Money(Decimal("10.00"), "EUR")
    m2 = Money(Decimal("5.00"), "EUR")
    result = m1 + m2
    assert result.amount == Decimal("15.00")


def test_money_add_different_currency_fails():
    m1 = Money(Decimal("10.00"), "EUR")
    m2 = Money(Decimal("5.00"), "USD")
    with pytest.raises(CurrencyMismatch):
        _ = m1 + m2


def test_money_subtract_below_zero_fails():
    m1 = Money(Decimal("10.00"), "EUR")
    m2 = Money(Decimal("20.00"), "EUR")
    with pytest.raises(InvariantViolation):
        _ = m1 - m2
