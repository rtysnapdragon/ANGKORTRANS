from rest_framework import serializers
from .models import Country, Province, District, Commune, Village, AdminAddress


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['CountryId', 'CountryCode', 'CountryNameEn', 'CountryNameKh', 
                  'PhoneCode', 'CurrencyCode', 'IsActive']
    CountryId = serializers.IntegerField(source='COUNTRY_ID', read_only=True)
    CountryCode = serializers.CharField(source='COUNTRY_CODE')
    CountryNameEn = serializers.CharField(source='COUNTRY_NAME_EN')
    CountryNameKh = serializers.CharField(source='COUNTRY_NAME_KH')
    PhoneCode = serializers.CharField(source='PHONE_CODE')
    CurrencyCode = serializers.CharField(source='CURRENCY_CODE')
    IsActive = serializers.BooleanField(source='IS_ACTIVE')


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['ProvinceId', 'ProvinceCode', 'ProvinceNameKh', 'ProvinceNameEn', 'Region']
    ProvinceId = serializers.IntegerField(source='PROVINCE_ID', read_only=True)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['DistrictId', 'Province', 'DistrictCode', 'DistrictNameKh', 'DistrictNameEn']
    DistrictId = serializers.IntegerField(source='DISTRICT_ID', read_only=True)


class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ['CommuneId', 'District', 'CommuneCode', 'CommuneNameKh', 'CommuneNameEn']
    CommuneId = serializers.IntegerField(source='COMMUNE_ID', read_only=True)


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['VillageId', 'Commune', 'VillageCode', 'VillageNameKh', 'VillageNameEn']
    VillageId = serializers.IntegerField(source='VILLAGE_ID', read_only=True)

from rest_framework import serializers
from .models import District, Commune, Village

# ====================== DISTRICT ======================
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['DistrictId', 'Province', 'DistrictCode', 'DistrictNameKh', 'DistrictNameEn']
        read_only_fields = ['DistrictId']

    DistrictId = serializers.IntegerField(source='DISTRICT_ID', read_only=True)
    Province = serializers.PrimaryKeyRelatedField(source='PROVINCE', queryset=Province.objects.all())
    DistrictCode = serializers.CharField(source='DISTRICT_CODE')
    DistrictNameKh = serializers.CharField(source='DISTRICT_NAME_KH')
    DistrictNameEn = serializers.CharField(source='DISTRICT_NAME_EN')


# ====================== COMMUNE ======================
class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ['CommuneId', 'District', 'CommuneCode', 'CommuneNameKh', 'CommuneNameEn']
        read_only_fields = ['CommuneId']

    CommuneId = serializers.IntegerField(source='COMMUNE_ID', read_only=True)
    District = serializers.PrimaryKeyRelatedField(source='DISTRICT', queryset=District.objects.all())
    CommuneCode = serializers.CharField(source='COMMUNE_CODE')
    CommuneNameKh = serializers.CharField(source='COMMUNE_NAME_KH')
    CommuneNameEn = serializers.CharField(source='COMMUNE_NAME_EN')


# ====================== VILLAGE ======================
class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['VillageId', 'Commune', 'VillageCode', 'VillageNameKh', 'VillageNameEn']
        read_only_fields = ['VillageId']

    VillageId = serializers.IntegerField(source='VILLAGE_ID', read_only=True)
    Commune = serializers.PrimaryKeyRelatedField(source='COMMUNE', queryset=Commune.objects.all())
    VillageCode = serializers.CharField(source='VILLAGE_CODE')
    VillageNameKh = serializers.CharField(source='VILLAGE_NAME_KH')
    VillageNameEn = serializers.CharField(source='VILLAGE_NAME_EN')

    
class AdminAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAddress
        fields = [
            'AdminAddressId', 'Country', 'Province', 'District', 'Commune', 'Village',
            'AddressLine1', 'AddressLine2', 'ZipCode', 'AddressType',
            'EntityType', 'EntityId', 'IsDefault', 'IsActive'
        ]
    AdminAddressId = serializers.IntegerField(source='ADMIN_ADDRESS_ID', read_only=True)
    Country = serializers.PrimaryKeyRelatedField(source='COUNTRY', queryset=Country.objects.all())
    Province = serializers.PrimaryKeyRelatedField(source='PROVINCE', queryset=Province.objects.all())
    District = serializers.PrimaryKeyRelatedField(source='DISTRICT', queryset=District.objects.all())
    Commune = serializers.PrimaryKeyRelatedField(source='COMMUNE', queryset=Commune.objects.all())
    Village = serializers.PrimaryKeyRelatedField(source='VILLAGE', queryset=Village.objects.all(), allow_null=True, required=False)
    
    AddressLine1 = serializers.CharField(source='ADDRESS_LINE1')
    AddressLine2 = serializers.CharField(source='ADDRESS_LINE2', required=False, allow_blank=True)
    ZipCode = serializers.CharField(source='ZIP_CODE', required=False, allow_blank=True)
    AddressType = serializers.ChoiceField(source='ADDRESS_TYPE', choices=AdminAddress._meta.get_field('ADDRESS_TYPE').choices)
    EntityType = serializers.ChoiceField(source='ENTITY_TYPE', choices=AdminAddress._meta.get_field('ENTITY_TYPE').choices)
    EntityId = serializers.IntegerField(source='ENTITY_ID')
    IsDefault = serializers.BooleanField(source='IS_DEFAULT')
    IsActive = serializers.BooleanField(source='IS_ACTIVE')
