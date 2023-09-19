from django.urls import path

from . import views


urlpatterns = [
    path('transactions/', views.TransactionsListView.as_view(), name='transactions.list'),
    path('transactions/new', views.TransactionsCreateView.as_view(), name='transactions.new'),
    path('transactions/edit/<int:pk>/', views.TransactionsUpdateView.as_view(), name='transaction.edit'),
    path('transactions/delete/<int:pk>/', views.TransactionsDeleteView.as_view(), name='transaction_delete'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]