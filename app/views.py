import logging
import traceback

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from app.models import Transaction
from app.serializers import TransactionSerializer

from messages import *


logger = logging.getLogger(__name__)


class TransactionBaseView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (AllowAny,)


class TransactionListView(TransactionBaseView):
    def get(self, request, **kwargs):
        try:
            date = timezone.now().strptime(
                "{}-{}-{}".format(
                    f"0{kwargs['day']}" if 0 <= kwargs['day'] <= 9 else kwargs['day'],
                    f"0{kwargs['month']}" if 0 <= kwargs['month'] <= 9 else kwargs['month'],
                    f"0{kwargs['year']}" if 0 <= kwargs['year'] <= 9 else kwargs['year'],
                ),
                "%d-%m-%y"
            ).date()

            queryset = self.get_queryset().filter(date=date)
            serialized_data = self.serializer_class(queryset, context=self.get_serializer_context(), many=True).data

            response = {
                "status": {
                    "code": status.HTTP_200_OK,
                    "message": TRANSACTION_LIST_SUCCESS.format(len(serialized_data), date.strftime('%d-%m-%y')),
                },
                "data": serialized_data,
            }

        except Exception as e:
            logger.error({'Ref': str(e), 'traceback': traceback.format_exc()})
            response = {
                "status": {
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": str(e),
                },
                "data": None,
            }

        return Response(response)


class BalanceAmountView(TransactionBaseView):
    def get(self, request, **kwargs):
        try:
            date = timezone.now().strptime(
                "{}-{}-{}".format(
                    f"0{kwargs['day']}" if 0 <= kwargs['day'] <= 9 else kwargs['day'],
                    f"0{kwargs['month']}" if 0 <= kwargs['month'] <= 9 else kwargs['month'],
                    f"0{kwargs['year']}" if 0 <= kwargs['year'] <= 9 else kwargs['year'],
                ),
                "%d-%m-%y"
            ).date()

            instance = self.get_queryset().filter(date=date).order_by('-sequence').first()
            response = {
                "status": {
                    "code": status.HTTP_200_OK,
                    "message": BALANCE_AMOUNT_SUCCESS.format('Balanced Amount' if instance else 'No Balance Amount',
                                                             date.strftime('%d-%m-%y')),
                },
                "balance_amount": instance.balance_amount if instance else None,
            }

        except Exception as e:
            logger.error({'Ref': str(e), 'traceback': traceback.format_exc()})
            response = {
                "status": {
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": str(e),
                },
                "balance_amount": None,
            }

        return Response(response)


class TransactionDetailView(TransactionBaseView):
    def get(self, request, **kwargs):
        instance = self.get_queryset().filter(id=kwargs['pk']).first()

        if instance:
            serialized_data = self.serializer_class(instance, context=self.get_serializer_context()).data
            response = {
                "status": {
                    "code": status.HTTP_200_OK,
                    "message": TRANSACTION_DETAIL_SUCCESS.format(kwargs['pk']),
                },
                "data": serialized_data,
            }
        else:
            response = {
                "status": {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": TRANSACTION_DETAIL_ERROR.format(kwargs['pk']),
                },
                "data": None,
            }

        return Response(response)


class TransactionCreateView(TransactionBaseView):
    @transaction.atomic
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = {
                "status": {
                    "code": status.HTTP_201_CREATED,
                    "message": TRANSACTION_CREATE_SUCCESS,
                },
                "data": serializer.data,
            }
        except Exception as e:
            logger.error({'Ref': str(e), 'traceback': traceback.format_exc()})
            response = {
                "status": {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": e.args[0],
                },
                "data": None,
            }

        return Response(response)
