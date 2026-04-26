# accounts/rbac/serializers.py
from rest_framework import serializers
from accounts.auth.models import Role, UserRole, Permission, RolePermission


class RoleSerializer(serializers.ModelSerializer):
    CreatedBy = serializers.SerializerMethodField(read_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.SerializerMethodField(read_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)
    
    class Meta:
        model = Role
        fields = [
            'ID', 'CODE', 'NAME', 'DESCRIPTION',
            'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt'
        ]
    
    def get_CreatedBy(self, obj):
        if obj.CREATED_BY:
            return {
                'ID': obj.CREATED_BY.id,
                'Username': getattr(obj.CREATED_BY, 'username', None),
                'Email': getattr(obj.CREATED_BY, 'email', None)
            }
        return None
    
    def get_UpdatedBy(self, obj):
        if obj.UPDATED_BY:
            return {
                'ID': obj.UPDATED_BY.id,
                'Username': getattr(obj.UPDATED_BY, 'username', None),
                'Email': getattr(obj.UPDATED_BY, 'email', None)
            }
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['CREATED_BY'] = request.user
            validated_data['UPDATED_BY'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['UPDATED_BY'] = request.user
        return super().update(instance, validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    CreatedBy = serializers.SerializerMethodField(read_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.SerializerMethodField(read_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)
    
    class Meta:
        model = Permission
        fields = [
            'ID', 'CODE', 'NAME', 'DESCRIPTION',
            'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt'
        ]
    
    def get_CreatedBy(self, obj):
        if obj.CREATED_BY:
            return {
                'ID': obj.CREATED_BY.id,
                'Username': getattr(obj.CREATED_BY, 'username', None)
            }
        return None
    
    def get_UpdatedBy(self, obj):
        if obj.UPDATED_BY:
            return {
                'ID': obj.UPDATED_BY.id,
                'Username': getattr(obj.UPDATED_BY, 'username', None)
            }
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['CREATED_BY'] = request.user
            validated_data['UPDATED_BY'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['UPDATED_BY'] = request.user
        return super().update(instance, validated_data)


class RolePermissionSerializer(serializers.ModelSerializer):
    Role = RoleSerializer(source='ROLE_ID', read_only=True)
    Permission = PermissionSerializer(source='PERMISSION_ID', read_only=True)
    RoleID = serializers.PrimaryKeyRelatedField(
        source='ROLE_ID', 
        queryset=Role.objects.all(), 
        write_only=True
    )
    PermissionID = serializers.PrimaryKeyRelatedField(
        source='PERMISSION_ID', 
        queryset=Permission.objects.all(), 
        write_only=True
    )
    CreatedBy = serializers.SerializerMethodField(read_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.SerializerMethodField(read_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = [
            'ID', 'Role', 'Permission', 'RoleID', 'PermissionID',
            'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt'
        ]
    
    def get_CreatedBy(self, obj):
        if obj.CREATED_BY:
            return {'ID': obj.CREATED_BY.id, 'Username': getattr(obj.CREATED_BY, 'username', None)}
        return None
    
    def get_UpdatedBy(self, obj):
        if obj.UPDATED_BY:
            return {'ID': obj.UPDATED_BY.id, 'Username': getattr(obj.UPDATED_BY, 'username', None)}
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['CREATED_BY'] = request.user
            validated_data['UPDATED_BY'] = request.user
        return super().create(validated_data)


class UserRoleSerializer(serializers.ModelSerializer):
    Role = RoleSerializer(source='ROLE_ID', read_only=True)
    UserID = serializers.PrimaryKeyRelatedField(
        source='USER_ID',
        queryset=None,  # Set in __init__
        write_only=True
    )
    RoleID = serializers.PrimaryKeyRelatedField(
        source='ROLE_ID',
        queryset=Role.objects.all(),
        write_only=True
    )
    CreatedBy = serializers.SerializerMethodField(read_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)
    UpdatedBy = serializers.SerializerMethodField(read_only=True)
    UpdatedAt = serializers.DateTimeField(source='UPDATED_AT', read_only=True)
    
    class Meta:
        model = UserRole
        fields = [
            'ID', 'UserID', 'RoleID', 'Role',
            'CreatedBy', 'CreatedAt', 'UpdatedBy', 'UpdatedAt'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set User queryset from settings.AUTH_USER_MODEL
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['UserID'].queryset = User.objects.all()
    
    def get_CreatedBy(self, obj):
        if obj.CREATED_BY:
            return {'ID': obj.CREATED_BY.id, 'Username': getattr(obj.CREATED_BY, 'username', None)}
        return None
    
    def get_UpdatedBy(self, obj):
        if obj.UPDATED_BY:
            return {'ID': obj.UPDATED_BY.id, 'Username': getattr(obj.UPDATED_BY, 'username', None)}
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['CREATED_BY'] = request.user
            validated_data['UPDATED_BY'] = request.user
        return super().create(validated_data)


class RoleDetailSerializer(RoleSerializer):
    """Role serializer with nested permissions."""
    Permissions = serializers.SerializerMethodField()
    
    class Meta(RoleSerializer.Meta):
        fields = RoleSerializer.Meta.fields + ['Permissions']
    
    def get_Permissions(self, obj):
        permissions = Permission.objects.filter(
            rolepermission__ROLE_ID=obj
        ).distinct()
        return PermissionSerializer(permissions, many=True).data