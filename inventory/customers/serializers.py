from rest_framework import serializers
from inventory.customers.models import Customer
from accounts.users.models import User

# ====================== CUSTOMER ======================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['CustomerId', 'CustomerCode', 'CustomerName', 'Phone', 'Email', 
                  'Address', 'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt']
        read_only_fields = ['CustomerId', 'CreatedAt', 'UpdatedAt']

    CustomerId = serializers.IntegerField(source='CUSTOMER_ID', read_only=True)
    CustomerCode = serializers.CharField(source='CUSTOMER_CODE')
    CustomerName = serializers.CharField(source='CUSTOMER_NAME')
    Phone = serializers.CharField(source='PHONE', required=False, allow_blank=True)
    Email = serializers.EmailField(source='EMAIL', required=False, allow_blank=True)
    Address = serializers.CharField(source='ADDRESS', required=False, allow_blank=True)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)