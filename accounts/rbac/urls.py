# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UserRoleViewSet, PermissionViewSet, 
    RolePermissionViewSet, UserViewSet
)

urlpatterns = [
    path('api/roles/', RoleViewSet.as_view({'get': 'list'})),  # List all roles
    # path('api/user', UserRoleViewSet),  # List user-role assignments
    # path('api/permission', PermissionViewSet),  # List all permissions
    # path('api/role-permission', RolePermissionViewSet),  # List role-permission assignments
    # path('api/user/assign-role', UserViewSet.assign_role),
]

# API Endpoints:
# GET     /api/role/                    - List all roles
# POST    /api/role/                    - Create role
# GET     /api/role/{id}/               - Get role details
# PUT     /api/role/{id}/               - Update role
# DELETE  /api/role/{id}/               - Delete role
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