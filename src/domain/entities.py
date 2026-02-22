from enum import Enum
from typing import List
from uuid import UUID, uuid4

from .value_objects import Money, IdempotencyKey
from .exceptions import InvariantViolation, InvalidStateTransition


class PaymentState(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    REQUIRES_ACTION = "requires_action"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Payment:
    def __init__(self, amount: Money, idempotency_key: IdempotencyKey):
        self.id = uuid4()
        self.amount = amount
        self.idempotency_key = idempotency_key
        self.state = PaymentState.CREATED
        self._events: List[str] = []

    def _transition(self, new_state: PaymentState):
        if not self._is_valid_transition(new_state):
            raise InvalidStateTransition(
                f"Cannot transition from {self.state} to {new_state}"
            )
        self.state = new_state
        self._events.append(f"transitioned_to_{new_state.value}")

    def _is_valid_transition(self, new_state: PaymentState) -> bool:
        allowed = {
            PaymentState.CREATED: {PaymentState.PROCESSING},
            PaymentState.PROCESSING: {
                PaymentState.REQUIRES_ACTION,
                PaymentState.SUCCEEDED,
                PaymentState.FAILED,
            },
            PaymentState.REQUIRES_ACTION: {
                PaymentState.PROCESSING,
                PaymentState.FAILED,
                PaymentState.CANCELLED,
            },
            PaymentState.SUCCEEDED: set(),
            PaymentState.FAILED: set(),
            PaymentState.CANCELLED: set(),
        }

        return new_state in allowed[self.state]
    
    @classmethod
    def rehydrate(
        cls,
        *,
        id,
        amount,
        idempotency_key,
        state,
    ):
        payment = cls(
            amount=amount,
            idempotency_key=idempotency_key,
        )
        payment.id = id
        payment.state = state
        return payment

    def mark_processing(self):
        self._transition(PaymentState.PROCESSING)

    def mark_requires_action(self):
        self._transition(PaymentState.REQUIRES_ACTION)

    def mark_succeeded(self):
        self._transition(PaymentState.SUCCEEDED)

    def mark_failed(self):
        self._transition(PaymentState.FAILED)

    def cancel(self):
        self._transition(PaymentState.CANCELLED)

    @property
    def events(self):
        return list(self._events)
