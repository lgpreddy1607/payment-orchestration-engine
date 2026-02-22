from decimal import Decimal

from django.test import TestCase

from domain.entities import Payment
from domain.value_objects import Money, IdempotencyKey
from infrastructure.repositories import PaymentRepository
from payments.models import PaymentModel


class PaymentRepositoryTest(TestCase):

    def test_idempotent_create(self):
        payment = Payment(
            amount=Money(Decimal("100.00"), "EUR"),
            idempotency_key=IdempotencyKey("abc123"),
        )

        # First creation
        created = PaymentRepository.create(payment)

        # Second creation with same idempotency key
        duplicate = PaymentRepository.create(payment)

        # Only one DB row should exist
        self.assertEqual(PaymentModel.objects.count(), 1)

        # Both returned objects should have same ID
        self.assertEqual(created.id, duplicate.id)