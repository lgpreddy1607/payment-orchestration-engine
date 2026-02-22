import uuid
from django.db import models


class PaymentModel(models.Model):
    class State(models.TextChoices):
        CREATED = "created", "Created"
        PROCESSING = "processing", "Processing"
        REQUIRES_ACTION = "requires_action", "Requires Action"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)

    state = models.CharField(
        max_length=32,
        choices=State.choices,
        default=State.CREATED,
    )

    idempotency_key = models.CharField(
        max_length=255,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"