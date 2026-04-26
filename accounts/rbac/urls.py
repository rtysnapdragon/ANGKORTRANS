# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UserRoleViewSet, PermissionViewSet, 
    RolePermissionViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'user-roles', UserRoleViewSet, basename='userrole')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'role-permissions', RolePermissionViewSet, basename='rolepermission')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]

# API Endpoints:
# GET     /api/roles/                    - List all roles
# POST    /api/roles/                    - Create role
# GET     /api/roles/{id}/               - Get role details
# PUT     /api/roles/{id}/               - Update role
# DELETE  /api/roles/{id}/               - Delete role
# GET     /api/roles/{id}/permissions/   - Get role permissions
# POST    /api/roles/{id}/assign_permission/ - Assign permission to role
#
# GET     /api/users/                    - List users
# GET     /api/users/{id}/roles/         - Get user roles
# POST    /api/users/{id}/assign_role/   - Assign role to user
#
# GET     /api/permissions/              - List permissions
# GET     /api/user-roles/               - List user-role assignments
# GET     /api/role-permissions/         - List role-permission assignments