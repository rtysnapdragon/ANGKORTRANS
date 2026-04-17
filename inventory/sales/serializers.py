from rest_framework import serializers


# ====================== SALE & DETAIL ======================
class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ['SaleDetailId', 'Product', 'Quantity', 'UnitPrice',
                  'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt']
        read_only_fields = ['SaleDetailId', 'CreatedAt', 'UpdatedAt']

    SaleDetailId = serializers.IntegerField(source='SALE_DETAIL_ID', read_only=True)
    Product = serializers.PrimaryKeyRelatedField(source='PRODUCT', queryset=Product.objects.all())
    Quantity = serializers.IntegerField(source='QUANTITY')
    UnitPrice = serializers.DecimalField(source='UNIT_PRICE', max_digits=15, decimal_places=2)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)


class SaleSerializer(serializers.ModelSerializer):
    Details = SaleDetailSerializer(many=True, write_only=True, source='details')

    class Meta:
        model = Sale
        fields = ['SaleId', 'SaleCode', 'Customer', 'SaleDate',
                  'TotalAmount', 'Discount', 'NetAmount', 'PaymentMethod',
                  'Status', 'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt', 'Details']
        read_only_fields = ['SaleId', 'NetAmount', 'CreatedAt', 'UpdatedAt']

    SaleId = serializers.IntegerField(source='SALE_ID', read_only=True)
    SaleCode = serializers.CharField(source='SALE_CODE')
    Customer = serializers.PrimaryKeyRelatedField(source='CUSTOMER', queryset=Customer.objects.all(), allow_null=True, required=False)
    SaleDate = serializers.DateField(source='SALE_DATE')
    TotalAmount = serializers.DecimalField(source='TOTAL_AMOUNT', max_digits=15, decimal_places=2)
    Discount = serializers.DecimalField(source='DISCOUNT', max_digits=15, decimal_places=2, default=0)
    NetAmount = serializers.DecimalField(source='NET_AMOUNT', read_only=True)
    PaymentMethod = serializers.ChoiceField(source='PAYMENT_METHOD', choices=Sale._meta.get_field('PAYMENT_METHOD').choices)
    Status = serializers.ChoiceField(source='STATUS', choices=Sale._meta.get_field('STATUS').choices)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)