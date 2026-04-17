from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Purchase
from .serializers import PurchaseSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from inventory.purchases.models import PurchaseDetail, Purchase, Product
from inventory.products.models import Product
from .serializers import PurchaseDetailSerializer


# ====================== LIST PURCHASE DETAILS ======================
@api_view(['POST'])
def purchase_detail_list(request):
    """List all purchase details - POST only"""
    if request.method == 'POST':
        purchase_details = PurchaseDetail.objects.all().order_by('-CREATED_AT')
        serializer = PurchaseDetailSerializer(purchase_details, many=True)
        return Response(serializer.data)


# ====================== CREATE PURCHASE DETAIL ======================
@api_view(['POST'])
def purchase_detail_create(request):
    """Create new purchase detail - POST"""
    if request.method == 'POST':
        serializer = PurchaseDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(CREATED_BY=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================== UPDATE PURCHASE DETAIL ======================
@api_view(['POST'])
def purchase_detail_update(request, pk):
    """Update purchase detail - POST"""
    purchase_detail = get_object_or_404(PurchaseDetail, pk=pk)
    
    if request.method == 'POST':
        serializer = PurchaseDetailSerializer(purchase_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(UPDATED_BY=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================== DELETE PURCHASE DETAIL ======================
@api_view(['GET'])
def purchase_detail_delete(request, pk):
    """Delete purchase detail - GET only"""
    purchase_detail = get_object_or_404(PurchaseDetail, pk=pk)
    
    if request.method == 'GET':
        purchase_detail.delete()
        return Response({"message": "Purchase detail deleted successfully"}, status=status.HTTP_200_OK)


# ====================== PURCHASE DETAIL BY PURCHASE ID ======================
@api_view(['POST'])
def purchase_detail_by_purchase(request, purchase_id):
    """Get all details for a specific purchase - POST"""
    if request.method == 'POST':
        details = PurchaseDetail.objects.filter(PURCHASE_id=purchase_id)
        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data)