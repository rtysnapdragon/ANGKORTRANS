from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Customer, Supplier, Product, Purchase, Sale, StockMovement
from .serializers import (
    CustomerSerializer, SupplierSerializer, ProductSerializer,
    PurchaseSerializer, SaleSerializer, StockMovementSerializer
)

class SupplierViewSet(CustomModelViewSet):
    queryset = Supplier.objects.all().order_by('-CREATED_AT')
    serializer_class = SupplierSerializer
