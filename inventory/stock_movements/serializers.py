from rest_framework import serializers



# ====================== STOCK MOVEMENT ======================
class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['MovementId', 'Product', 'MovementType', 'Quantity',
                  'ReferenceId', 'ReferenceType', 'Notes', 'CreatedBy',
                  'CreatedAt', 'UpdatedBy', 'UpdatedAt']
        read_only_fields = ['MovementId', 'CreatedAt', 'UpdatedAt']

    MovementId = serializers.IntegerField(source='MOVEMENT_ID', read_only=True)
    Product = serializers.PrimaryKeyRelatedField(source='PRODUCT', queryset=Product.objects.all())
    MovementType = serializers.ChoiceField(source='MOVEMENT_TYPE', choices=StockMovement._meta.get_field('MOVEMENT_TYPE').choices)
    Quantity = serializers.IntegerField(source='QUANTITY')
    ReferenceId = serializers.IntegerField(source='REFERENCE_ID', required=False, allow_null=True)
    ReferenceType = serializers.CharField(source='REFERENCE_TYPE', required=False, allow_blank=True)
    Notes = serializers.CharField(source='NOTES', required=False, allow_blank=True)
    CreatedBy = serializers.PrimaryKeyRelatedField(source='CREATED_BY', queryset=User.objects.all(), write_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.PrimaryKeyRelatedField(source='UPDATED_BY', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)