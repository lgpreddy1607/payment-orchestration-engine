from django.db import transaction
from django.db.utils import IntegrityError

from payments.models import PaymentModel
from domain.entities import Payment
from domain.value_objects import Money, IdempotencyKey
from domain.entities import PaymentState


class PaymentRepository:

    @staticmethod
    def create(payment: Payment) -> Payment:
        try:
            with transaction.atomic():
                model = PaymentModel.objects.create(
                    id=payment.id,
                    amount=payment.amount.amount,
                    currency=payment.amount.currency,
                    state=payment.state.value,
                    idempotency_key=payment.idempotency_key.value,
                )
        except IntegrityError:
            model = PaymentModel.objects.get(
                idempotency_key=payment.idempotency_key.value
            )

        return PaymentRepository._to_domain(model)

    @staticmethod
    def _to_domain(model: PaymentModel) -> Payment:
        return Payment.rehydrate(
            id=model.id,
            amount=Money(model.amount, model.currency),
            idempotency_key=IdempotencyKey(model.idempotency_key),
            state=PaymentState(model.state),
        )