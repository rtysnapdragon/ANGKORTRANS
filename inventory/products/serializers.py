from rest_framework import serializers
from accounts.users.models import ( Users)
from inventory.products.models import ( Product,ProductDetail )
from inventory.purchases.models import ( PurchaseDetail)


# ====================== PRODUCT ======================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['ProductId', 'ProductCode', 'ProductName', 'Category', 'Unit',
                  'PurchasePrice', 'SalePrice', 'CurrentStock', 'MinStock',
                  'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt']
        read_only_fields = ['ProductId', 'CurrentStock', 'CreatedAt', 'UpdatedAt']

    ProductId = serializers.IntegerField(source='ID', read_only=True)
    ProductCode = serializers.CharField(source='CODE')
    ProductName = serializers.CharField(source='NAME')
    Category = serializers.CharField(source='CATEGORY', required=False, allow_blank=True)
    Unit = serializers.CharField(source='UNIT')
    PurchasePrice = serializers.DecimalField(source='PURCHASE_PRICE', max_digits=15, decimal_places=2)
    SalePrice = serializers.DecimalField(source='SALE_PRICE', max_digits=15, decimal_places=2)
    CurrentStock = serializers.IntegerField(source='CURRENT_STOCK', read_only=True)
    MinStock = serializers.IntegerField(source='MIN_STOCK')
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=Users.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=Users.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)


# ====================== PURCHASE & DETAIL ======================

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            'ProductDetailId', 'Product', 'Description', 'Specifications',
            'ImageUrl', 'Barcode', 'Location', 'ExpiryDate', 'Notes',
            'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt'
        ]
        read_only_fields = ['ProductDetailId', 'CreatedAt', 'UpdatedAt']

    ProductDetailId = serializers.IntegerField(source='ID', read_only=True)
    Product_Id = serializers.PrimaryKeyRelatedField(source='PRODUCT_ID', queryset=Product.objects.all())
    Description = serializers.CharField(source='DESCRIPTION', required=False, allow_blank=True)
    Specifications = serializers.JSONField(source='SPECIFICATIONS', required=False)
    ImageUrl = serializers.URLField(source='IMAGE_URL', required=False, allow_blank=True)
    Barcode = serializers.CharField(source='BARCODE', required=False, allow_blank=True)
    Location = serializers.CharField(source='LOCATION', required=False, allow_blank=True)
    ExpiryDate = serializers.DateField(source='EXPIRY_DATE', required=False, allow_null=True)
    Notes = serializers.CharField(source='NOTES', required=False, allow_blank=True)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=Users.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=Users.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)