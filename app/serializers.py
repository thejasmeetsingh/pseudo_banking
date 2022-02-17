import decimal

from rest_framework import serializers

from app.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'account_number',
            'date',
            'details',
            'value_date',
            'withdrawal_amount',
            'deposit_amount',
            'balance_amount',
        )

    def create(self, validated_data):
        if ('withdrawal_amount' not in validated_data and 'deposit_amount' not in validated_data) or \
                (('withdrawal_amount' in validated_data and not validated_data['withdrawal_amount']) and
                 ('deposit_amount' in validated_data and not validated_data['deposit_amount'])):
            raise serializers.ValidationError(
                'You need to send either Withdrawal Amount or Deposit Amount while adding Transaction Details',
                code='invalid',
            )

        is_balance_calculated = False

        if 'withdrawal_amount' in validated_data and validated_data['withdrawal_amount']:
            latest_transaction = Transaction.objects.filter(
                account_number=validated_data['account_number']
            ).order_by('-sequence').first()

            if latest_transaction:
                if not latest_transaction.balance_amount:
                    raise serializers.ValidationError('You do not have enough balance in your account.', code='invalid')

                balance_amount = latest_transaction.balance_amount + (
                    validated_data['deposit_amount']
                    if 'deposit_amount' not in validated_data and validated_data['deposit_amount']
                    else round(decimal.Decimal(0), 2)
                )

                if validated_data['withdrawal_amount'] > balance_amount:
                    raise serializers.ValidationError(
                        f"You can only without {validated_data['withdrawal_amount'] - balance_amount} from your account",
                        code='invalid',
                    )

                validated_data['balance_amount'] = balance_amount - validated_data['withdrawal_amount']
                is_balance_calculated = True

        if 'deposit_amount' in validated_data and validated_data['deposit_amount'] and not is_balance_calculated:
            latest_transaction = Transaction.objects.filter(
                account_number=validated_data['account_number']
            ).order_by('-sequence').first()

            if latest_transaction and latest_transaction.balance_amount:
                validated_data['balance_amount'] = latest_transaction.balance_amount + validated_data['deposit_amount']
            else:
                validated_data['balance_amount'] = validated_data['deposit_amount']

        validated_data['sequence'] = Transaction.objects.count() + 1
        return super().create(validated_data)
