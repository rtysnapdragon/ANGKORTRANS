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

class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """Stock movements remain read-only with POST for list"""
    queryset = StockMovement.objects.all().order_by('-CREATED_AT')
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)