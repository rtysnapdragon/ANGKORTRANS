from rest_framework import serializers


# ====================== SUPPLIER ======================
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['SupplierId', 'SupplierCode', 'SupplierName', 'Phone', 'Email', 
                  'Address', 'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt']
        read_only_fields = ['SupplierId', 'CreatedAt', 'UpdatedAt']

    SupplierId = serializers.IntegerField(source='SUPPLIER_ID', read_only=True)
    SupplierCode = serializers.CharField(source='SUPPLIER_CODE')
    SupplierName = serializers.CharField(source='SUPPLIER_NAME')
    Phone = serializers.CharField(source='PHONE', required=False)
    Email = serializers.EmailField(source='EMAIL', required=False)
    Address = serializers.CharField(source='ADDRESS', required=False)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)