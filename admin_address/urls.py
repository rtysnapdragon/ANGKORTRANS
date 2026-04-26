from django.urls import path
from .views import (
    # Country
    country_list, country_create, country_update, country_delete,
    # District
    district_list, district_create, district_update, district_delete,
    # Commune
    commune_list, commune_create, commune_update, commune_delete,
    # Village
    village_list, village_create, village_update, village_delete,
    # Admin Address
    admin_address_list, admin_address_create, admin_address_update, admin_address_delete,
)

urlpatterns = [
    # ==================== COUNTRY ====================
    path('api/country/list', country_list, name='country-list'),
    path('api/country/create', country_create, name='country-create'),
    path('api/country/update', country_update, name='country-update'),
    path('api/country/delete', country_delete, name='country-delete'),

    # ==================== DISTRICT ====================
    path('api/district/list', district_list, name='district-list'),
    path('api/district/create', district_create, name='district-create'),
    path('api/district/update', district_update, name='district-update'),
    path('api/district/delete', district_delete, name='district-delete'),

    # ==================== COMMUNE ====================
    path('api/commune/list', commune_list, name='commune-list'),
    path('api/commune/create', commune_create, name='commune-create'),
    path('api/commune/update', commune_update, name='commune-update'),
    path('api/commune/delete', commune_delete, name='commune-delete'),

    # ==================== VILLAGE ====================
    path('api/village/list', village_list, name='village-list'),
    path('api/village/create', village_create, name='village-create'),
    path('api/village/update', village_update, name='village-update'),
    path('api/village/delete', village_delete, name='village-delete'),

    # ==================== ADMIN ADDRESS ====================
    path('api/admin_address/list', admin_address_list, name='admin_address-list'),
    path('api/admin_address/create', admin_address_create, name='admin_address-create'),
    path('api/admin_address/update', admin_address_update, name='admin_address-update'),
    path('api/admin_address/delete', admin_address_delete, name='admin_address-delete'),
]