from rest_framework import serializers
from admin_address.models import Country, Province, District, Commune, Village
from .models import (
    Users as User,UserProfile
)


class UserProfileSerializer(serializers.ModelSerializer):
    IsVerified = serializers.BooleanField(source='IS_VERIFIED')
    class Meta:
        model = UserProfile
        fields = [
            'Name', 'NameEnglish', 'Gender', 'Dob', 'NationalId',
            'Country', 'Province', 'District', 'Commune', 'Village',
            'AddressLine1', 'AddressLine2', 'ZipCode', 'PostalCode',
            'ProfilePictureUrl', 'LanguagePreference', 'IsVerified'
        ]

    Name = serializers.CharField(source='NAME')
    NameEnglish = serializers.CharField(source='NAME_ENGLISH')
    Gender = serializers.CharField(source='GENDER')
    Dob = serializers.DateField(source='DOB')
    NationalId = serializers.CharField(source='NATIONAL_ID')
    Country = serializers.PrimaryKeyRelatedField(source='COUNTRY_ID', queryset=Country.objects.all())
    Province = serializers.PrimaryKeyRelatedField(source='PROVINCE_ID', queryset=Province.objects.all(), allow_null=True)
    District = serializers.PrimaryKeyRelatedField(source='DISTRICT_ID', queryset=District.objects.all(), allow_null=True)
    Commune = serializers.PrimaryKeyRelatedField(source='COMMUNE_ID', queryset=Commune.objects.all(), allow_null=True)
    Village = serializers.PrimaryKeyRelatedField(source='VILLAGE_ID', queryset=Village.objects.all(), allow_null=True)
    AddressLine1 = serializers.CharField(source='ADDRESS_LINE1')
    AddressLine2 = serializers.CharField(source='ADDRESS_LINE2', required=False)
    ZipCode = serializers.CharField(source='ZIP_CODE', required=False)
    PostalCode = serializers.CharField(source='POSTAL_CODE', required=False)
    ProfilePictureUrl = serializers.URLField(source='PROFILE_PICTURE_URL', required=False)
    LanguagePreference = serializers.CharField(source='LANGUAGE_PREFERENCE')





# ====================== USER ======================
class UserSerializer(serializers.ModelSerializer):
    Profile = UserProfileSerializer(source='userprofile', read_only=True)
    class Meta:
        model = User
        fields = [
            'Id', 'Code', 'Username', 'Email', 'UserType',
            'EmailVerified', 'PhoneVerified', 'Status', 'IsSuperuser',
            'LastLogin', 'CreatedAt','Profile'
        ]
        read_only_fields = ['Id', 'CreatedAt', 'LastLogin']

    Id = serializers.IntegerField(source='ID', read_only=True)
    Code = serializers.CharField(source='CODE')
    Username = serializers.CharField(source='USERNAME')
    Email = serializers.EmailField(source='EMAIL')
    UserType = serializers.CharField(source='USER_TYPE')
    EmailVerified = serializers.BooleanField(source='EMAIL_VERIFIED')
    PhoneVerified = serializers.BooleanField(source='PHONE_VERIFIED')
    Status = serializers.CharField(source='STATUS')
    IsSuperuser = serializers.BooleanField(source='IS_SUPERUSER')
    LastLogin = serializers.DateTimeField(source='LAST_LOGIN', read_only=True)
    CreatedAt = serializers.DateTimeField(source='CREATED_AT', read_only=True)

