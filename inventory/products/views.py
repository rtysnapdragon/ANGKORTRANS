from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ( ProductSerializer)
from inventory.customers.views import ( CustomerModelViewSet)


# ====================== LIST PRODUCTS (POST only) ======================
@api_view(['POST'])
def product_list(request):
    """List all products - Use POST method"""
    if request.method == 'POST':
        products = Product.objects.all().order_by('CODE')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# ====================== CREATE PRODUCT (POST) ======================
@api_view(['POST'])
def product_create(request):
    """Create new product - Use POST"""
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # Set audit field
            serializer.save(CREATED_BY=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================== UPDATE PRODUCT (POST) ======================
@api_view(['POST'])
def product_update(request, pk):
    """Update product - Use POST (pk in URL)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(UPDATED_BY=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================== DELETE PRODUCT (GET) ======================
@api_view(['GET'])
def product_delete(request, pk):
    """Delete product - Use GET (pk in URL)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)


# ====================== LOW STOCK (POST) ======================
@api_view(['POST'])
def product_low_stock(request):
    """Low stock report - Use POST"""
    if request.method == 'POST':
        low_products = Product.objects.filter(CURRENT_STOCK__lt=models.F('MIN_STOCK'))
        serializer = ProductSerializer(low_products, many=True)
        return Response(serializer.data)


# Example: inventory/products/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api_app.utils.db_connection import register_dynamic_database, mysql_connection
from .models import Product   # Your models


@api_view(['POST'])
def product_list_dynamic(request):
    """List products from any database name sent in request"""
    db_name = request.data.get('DatabaseName')   # e.g., "angkortrans_client1"

    if not db_name:
        return Response({"Message": "DatabaseName is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        alias = register_dynamic_database(db_name)

        # Use Django ORM with dynamic database
        products = Product.objects.using(alias).all().order_by('PRODUCT_CODE')[:50]

        # If you have serializer
        # serializer = ProductSerializer(products, many=True)
        # return Response(serializer.data)

        data = [{"ProductCode": p.PRODUCT_CODE, "ProductName": p.PRODUCT_NAME, "CurrentStock": p.CURRENT_STOCK} 
                for p in products]

        return Response({
            "Database": db_name,
            "Alias": alias,
            "Products": data
        })

    except Exception as e:
        return Response({"Message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def raw_query_dynamic(request):
    """Raw SQL example with dynamic database name"""
    db_name = request.data.get('DatabaseName')

    try:
        with get_raw_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT PRODUCT_CODE, PRODUCT_NAME, CURRENT_STOCK FROM PRODUCT LIMIT 20")
                rows = cursor.fetchall()

        return Response({
            "Database": db_name,
            "Rows": rows
        })

    except Exception as e:
        return Response({"Message": f"Connection failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)