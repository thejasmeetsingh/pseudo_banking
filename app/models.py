import uuid

from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True, db_index=True)
    account_number = models.PositiveBigIntegerField()
    date = models.DateField()
    details = models.CharField(max_length=255)
    value_date = models.DateField()
    withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('account_number', 'date')
