from django.urls import path

from app import views

urlpatterns = [
    path('transactions/<int:day>-<int:month>-<int:year>/', views.TransactionListView.as_view()),
    path('balance/<int:day>-<int:month>-<int:year>/', views.BalanceAmountView.as_view()),
    path('details/<str:pk>/', views.TransactionDetailView.as_view()),
]
