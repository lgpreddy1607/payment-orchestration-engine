import pytest
from decimal import Decimal

from domain.entities import Payment, PaymentState
from domain.value_objects import Money
from domain.exceptions import InvalidStateTransition
from domain.value_objects import Money, IdempotencyKey


def create_payment():
    return Payment(
        amount=Money(Decimal("100.00"), "EUR"),
        idempotency_key=IdempotencyKey("abc123"),
    )


def test_initial_state_is_created():
    payment = create_payment()
    assert payment.state == PaymentState.CREATED


def test_valid_transition_created_to_processing():
    payment = create_payment()
    payment.mark_processing()
    assert payment.state == PaymentState.PROCESSING


def test_invalid_transition_created_to_succeeded_fails():
    payment = create_payment()
    with pytest.raises(InvalidStateTransition):
        payment.mark_succeeded()


def test_terminal_state_cannot_transition():
    payment = create_payment()
    payment.mark_processing()
    payment.mark_succeeded()

    with pytest.raises(InvalidStateTransition):
        payment.mark_failed()


def test_event_log_records_transitions():
    payment = create_payment()
    payment.mark_processing()
    payment.mark_succeeded()

    assert payment.events == [
        "transitioned_to_processing",
        "transitioned_to_succeeded",
    ]
