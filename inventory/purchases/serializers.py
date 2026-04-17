from rest_framework import serializers
from inventory.purchases.models import PurchaseDetail, Purchase
from accounts.users.models import User
from inventory.products.models import Product
from inventory.suppliers.models import Supplier



class PurchaseDetailSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseDetail with PascalCase fields"""
    
    PurchaseDetailId = serializers.IntegerField(source='PURCHASE_DETAIL_ID', read_only=True)
    Purchase = serializers.PrimaryKeyRelatedField(source='PURCHASE', queryset=Purchase.objects.all())
    Product = serializers.PrimaryKeyRelatedField(source='PRODUCT', queryset=Product.objects.all())
    Quantity = serializers.IntegerField(source='QUANTITY')
    UnitPrice = serializers.DecimalField(source='UNIT_PRICE', max_digits=15, decimal_places=2)
    Subtotal = serializers.DecimalField(source='SUBTOTAL', max_digits=15, decimal_places=2, read_only=True)
    
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = [
            'PurchaseDetailId',
            'Purchase',
            'Product',
            'Quantity',
            'UnitPrice',
            'Subtotal',
            'CreatedBy',
            'CreatedAt',
            'UpdatedBy',
            'UpdatedAt'
        ]
        read_only_fields = ['PurchaseDetailId', 'Subtotal', 'CreatedAt', 'UpdatedAt']

    def create(self, validated_data):
        # Auto calculate Subtotal
        quantity = validated_data.get('QUANTITY')
        unit_price = validated_data.get('UNIT_PRICE')
        if quantity and unit_price:
            validated_data['SUBTOTAL'] = quantity * unit_price
        return super().create(validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    Details = PurchaseDetailSerializer(many=True, write_only=True, source='details')

    class Meta:
        model = Purchase
        fields = ['Id', 'Code', 'Supplier', 'Date',
                  'TotalAmount', 'Status', 'CreatedBy', 'CreatedAt',
                  'UpdatedBy', 'UpdatedAt', 'Details']
        read_only_fields = ['Id', 'TotalAmount', 'CreatedAt', 'UpdatedAt']

    PurchaseId = serializers.IntegerField(source='ID', read_only=True)
    PurchaseCode = serializers.CharField(source='CODE')
    Supplier = serializers.PrimaryKeyRelatedField(source='SUPPLIER', queryset=Supplier.objects.all())
    PurchaseDate = serializers.DateField(source='DATE')
    TotalAmount = serializers.DecimalField(source='TOTAL_AMOUNT', max_digits=15, decimal_places=2, read_only=True)
    Status = serializers.ChoiceField(source='STATUS', choices=Purchase._meta.get_field('STATUS').choices)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)


