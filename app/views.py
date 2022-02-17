import logging
import traceback

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from app.models import Transaction
from app.serializers import TransactionSerializer


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
                    "message": f"{len(serialized_data)} transactions found for {date.strftime('%d-%m-%y')} date."
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
