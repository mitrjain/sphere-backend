from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list),
    path('transactions/<int:pk>/', views.transaction_detail),
    path('tax-liability/', views.tax_liability),
]
