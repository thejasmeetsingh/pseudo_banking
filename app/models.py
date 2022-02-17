import uuid

from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, db_index=True, editable=False)
    account_number = models.PositiveBigIntegerField()
    date = models.DateField()
    details = models.CharField(max_length=255)
    value_date = models.DateField()
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # For fetching latest transaction if the date of one or more transactions is the same.
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('account_number', 'date')
