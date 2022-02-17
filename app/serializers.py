from rest_framework import serializers

from app.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'account_number',
            'date',
            'details',
            'value_date',
            'withdrawal_amount',
            'deposit_amount',
            'balance_amount',
        )
