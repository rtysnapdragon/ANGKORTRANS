# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import connections
from django.utils import timezone
from accounts.auth.models import Role, UserRole, Permission, RolePermission
from .serializers import (
    RoleSerializer, UserRoleSerializer, 
    PermissionSerializer, RolePermissionSerializer, UserSerializer
)
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class DynamicDatabaseMixin:
    """Mixin to handle dynamic database connections"""
    
    def _set_database_alias(self, request):
        """Set database alias from request header or query param"""
        db_alias = request.headers.get('X-Database-Alias', None)
        if not db_alias:
            db_alias = request.query_params.get('db_alias', 'default')
        
        request.db_alias = db_alias
        return db_alias
    
    def get_queryset(self):
        """Get queryset with dynamic database"""
        db_alias = self._set_database_alias(self.request)
        
        if hasattr(self, 'model'):
            return self.model.objects.using(db_alias).all()
        return super().get_queryset()
    
    def perform_create(self, serializer):
        """Perform create with dynamic database and audit fields"""
        db_alias = getattr(self.request, 'db_alias', 'default')
        
        # Set audit fields
        if self.request.user.is_authenticated:
            serializer.save(
                CREATED_BY=self.request.user,
                UPDATED_BY=self.request.user
            )
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        """Perform update with dynamic database and audit fields"""
        if self.request.user.is_authenticated:
            serializer.save(UPDATED_BY=self.request.user, UPDATED_AT=timezone.now())
        else:
            serializer.save()


class RoleViewSet(DynamicDatabaseMixin, viewsets.ModelViewSet):
    """ViewSet for Role management"""
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    model = Role
    
    def get_queryset(self):
        db_alias = self._set_database_alias(self.request)
        return Role.objects.using(db_alias).all()
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Get all permissions for a role"""
        db_alias = self._set_database_alias(request)
        role = self.get_object()
        role_permissions = RolePermission.objects.using(db_alias).filter(ROLE_ID=role)
        permissions = [rp.PERMISSION_ID for rp in role_permissions]
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_permission(self, request, pk=None):
        """Assign permission to role"""
        db_alias = self._set_database_alias(request)
        role = self.get_object()
        permission_id = request.data.get('PERMISSION_ID')
        
        try:
            permission = Permission.objects.using(db_alias).get(ID=permission_id)
            
            with transaction.using(db_alias):
                role_permission, created = RolePermission.objects.using(db_alias).get_or_create(
                    ROLE_ID=role,
                    PERMISSION_ID=permission,
                    defaults={
                        'CREATED_BY': request.user,
                        'UPDATED_BY': request.user
                    }
                )
                
                if not created:
                    return Response(
                        {'error': 'Permission already assigned to this role'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                serializer = RolePermissionSerializer(role_permission)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Permission.DoesNotExist:
            return Response(
                {'error': 'Permission not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserRoleViewSet(DynamicDatabaseMixin, viewsets.ModelViewSet):
    """ViewSet for UserRole management"""
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]
    model = UserRole
    
    def get_queryset(self):
        db_alias = self._set_database_alias(self.request)
        return UserRole.objects.using(db_alias).all()
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get roles for a specific user"""
        db_alias = self._set_database_alias(request)
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_roles = UserRole.objects.using(db_alias).filter(USER_ID=user_id)
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Get users for a specific role"""
        db_alias = self._set_database_alias(request)
        role_id = request.query_params.get('role_id')
        
        if not role_id:
            return Response(
                {'error': 'role_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_roles = UserRole.objects.using(db_alias).filter(ROLE_ID=role_id)
        serializer = self.get_serializer(user_roles, many=True)
        return Response(serializer.data)


class PermissionViewSet(DynamicDatabaseMixin, viewsets.ModelViewSet):
    """ViewSet for Permission management"""
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    model = Permission
    
    def get_queryset(self):
        db_alias = self._set_database_alias(self.request)
        return Permission.objects.using(db_alias).all()
    
    @action(detail=True, methods=['get'])
    def roles(self, request, pk=None):
        """Get all roles that have this permission"""
        db_alias = self._set_database_alias(request)
        permission = self.get_object()
        role_permissions = RolePermission.objects.using(db_alias).filter(PERMISSION_ID=permission)
        roles = [rp.ROLE_ID for rp in role_permissions]
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)


class RolePermissionViewSet(DynamicDatabaseMixin, viewsets.ModelViewSet):
    """ViewSet for RolePermission management"""
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]
    model = RolePermission
    
    def get_queryset(self):
        db_alias = self._set_database_alias(self.request)
        return RolePermission.objects.using(db_alias).all()
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Get permissions for a specific role"""
        db_alias = self._set_database_alias(request)
        role_id = request.query_params.get('role_id')
        
        if not role_id:
            return Response(
                {'error': 'role_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        role_permissions = RolePermission.objects.using(db_alias).filter(ROLE_ID=role_id)
        serializer = self.get_serializer(role_permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_permission(self, request):
        """Get roles for a specific permission"""
        db_alias = self._set_database_alias(request)
        permission_id = request.query_params.get('permission_id')
        
        if not permission_id:
            return Response(
                {'error': 'permission_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        role_permissions = RolePermission.objects.using(db_alias).filter(PERMISSION_ID=permission_id)
        serializer = self.get_serializer(role_permissions, many=True)
        return Response(serializer.data)


class UserViewSet(DynamicDatabaseMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet for User (read-only)"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    model = User
    
    def get_queryset(self):
        db_alias = self._set_database_alias(self.request)
        return User.objects.using(db_alias).all()
    
    @action(detail=True, methods=['get'])
    def roles(self, request, pk=None):
        """Get all roles for a user"""
        db_alias = self._set_database_alias(request)
        user = self.get_object()
        user_roles = UserRole.objects.using(db_alias).filter(USER_ID=user)
        roles = [ur.ROLE_ID for ur in user_roles]
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        """Assign role to user"""
        db_alias = self._set_database_alias(request)
        user = self.get_object()
        role_id = request.data.get('ROLE_ID')
        
        try:
            role = Role.objects.using(db_alias).get(ID=role_id)
            
            with transaction.using(db_alias):
                user_role, created = UserRole.objects.using(db_alias).get_or_create(
                    USER_ID=user,
                    ROLE_ID=role,
                    defaults={
                        'CREATED_BY': request.user,
                        'UPDATED_BY': request.user
                    }
                )
                
                if not created:
                    return Response(
                        {'error': 'Role already assigned to this user'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                serializer = UserRoleSerializer(user_role)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Role.DoesNotExist:
            return Response(
                {'error': 'Role not found'},
                status=status.HTTP_404_NOT_FOUND
            )