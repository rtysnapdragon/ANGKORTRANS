from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.products.views import (
    product_list,
    product_create,
    product_update,
    product_delete,
    product_low_stock
)
from inventory.purchases.views import (
    purchase_detail_list,
    purchase_detail_create,
    purchase_detail_update,
    purchase_detail_delete,
    purchase_detail_by_purchase
)

urlpatterns = [
    # List Products → POST
    path('api/products/list', product_list, name='product-list'),

    # Create Product → POST
    path('api/products/create', product_create, name='product-create'),

    # Update Product → POST
    path('api/products/update', product_update, name='product-update'),

    # Delete Product → GET
    path('api/products/delete', product_delete, name='product-delete'),

    # Low Stock → POST
    path('api/products/low_stock', product_low_stock, name='product-low-stock'),

    # List all Purchase Details → POST
    path('api/purchase-details/list/', purchase_detail_list, name='purchase-detail-list'),

    # Create Purchase Detail → POST
    path('api/purchase-details/create/', purchase_detail_create, name='purchase-detail-create'),

    # Update Purchase Detail → POST
    path('api/purchase-details/update/<int:pk>/', purchase_detail_update, name='purchase-detail-update'),

    # Delete Purchase Detail → GET
    path('api/purchase-details/delete/<int:pk>/', purchase_detail_delete, name='purchase-detail-delete'),

    # Get Details by Purchase ID → POST
    path('api/purchase-details/by-purchase/<int:purchase_id>/', purchase_detail_by_purchase, name='purchase-detail-by-purchase'),
]