from django.urls import path

from app import views

urlpatterns = [
    path('transactions/<int:day>-<int:month>-<int:year>/', views.TransactionListView.as_view()),
]
