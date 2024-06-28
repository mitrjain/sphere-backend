from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sqlalchemy.orm import Session
from sqlalchemy_config import get_db
from .models import Transaction, LineItem, Address, TaxLiability
from .serializers import TransactionSerializer, LineItemSerializer, AddressSerializer, TaxLiabilitySerializer

@api_view(['GET'])
def transaction_list(request):
    db: Session = next(get_db())

    if request.method == 'GET':
        transactions = db.query(Transaction).all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def transaction_detail(request, pk):
    db: Session = next(get_db())
    
    transaction = db.query(Transaction).filter_by(id=pk).first()
    
    if transaction==None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

@api_view(['GET'])
def tax_liability(request):
    db: Session = next(get_db())
    
    tax = db.query(TaxLiability).first()
    
    if tax==None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaxLiabilitySerializer(tax)
        return Response(serializer.data)