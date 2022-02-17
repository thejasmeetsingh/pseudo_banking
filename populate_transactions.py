import decimal

import requests

from django.utils import timezone

from app.models import Transaction


def populate_transactions():
    """
    The purpose of this function is to populate given transactions onto the database.
    """

    response = requests.get(url='https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json').json()

    Transaction.objects.bulk_create([
        Transaction(
            account_number=data["Account No"],
            date=timezone.now().strptime(data["Date"], '%d %b %y').date(),
            details=data["Transaction Details"],
            value_date=timezone.now().strptime(data["Value Date"], '%d %b %y').date(),
            withdrawal_amount=round(decimal.Decimal(data["Withdrawal AMT"].replace(',', '')), 2)
            if data["Withdrawal AMT"] else 0.00,
            deposit_amount=round(decimal.Decimal(data["Deposit AMT"].replace(',', '')), 2)
            if data["Deposit AMT"] else 0.00,
            balance_amount=round(decimal.Decimal(data["Balance AMT"].replace(',', '')), 2)
            if data["Balance AMT"] else 0.00,
            sequence=sequence,
        )
        for sequence, data in enumerate(response)
    ])

    return 'Transaction Populated Successfully'
