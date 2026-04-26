from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import check_password, make_password
# from admin_address.models import Country, Province, District, Commune, Village
from django.db import models
from django.utils import timezone
from django.conf import settings

class Users(models.Model): # Can cause error due to circular import when User model is referenced in other models for foreign key relationships. To avoid this, we can use a string reference 'self' in the ForeignKey fields instead of directly referencing the User model. This allows Django to resolve the reference at runtime without causing import issues.
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'
        LOCKED = 'LOCKED'
        PENDING = 'PENDING'
        SUSPENDED = 'SUSPENDED'
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=15, unique=True,db_column='CODE')
    USERNAME = models.CharField(max_length=255, unique=True, db_column='USERNAME')
    EMAIL = models.EmailField(max_length=255, unique=True, db_column='EMAIL')
    PASSWORD_HASH = models.CharField(max_length=255, db_column='PASSWORD_HASH')
    USER_TYPE = models.CharField(max_length=20, default='USER', db_column='USER_TYPE')
    EMAIL_VERIFIED = models.BooleanField(default=False, db_column='EMAIL_VERIFIED')
    PHONE_VERIFIED = models.BooleanField(default=False, db_column='PHONE_VERIFIED')

    STATUS = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)  # ACTIVE, INACTIVE, LOCKED, PENDING
    IS_SUPERUSER = models.BooleanField(default=False, db_column='IS_SUPERUSER')
    FAILED_LOGIN_ATTEMPTS = models.IntegerField(default=0, db_column='FAILED_LOGIN_ATTEMPTS')
    LOCKED_UNTIL = models.DateTimeField(max_length=6, null=True, blank=True, db_column='LOCKED_UNTIL')
    LAST_LOGIN = models.DateTimeField(max_length=6, null=True, blank=True, db_column='LAST_LOGIN')
    PASSWORD_CHANGED_AT = models.DateTimeField(max_length=6, null=True, blank=True, db_column='PASSWORD_CHANGED_AT')

    IS_DELETED = models.BooleanField(default=False, db_column='IS_DELETED')
    
    # Audit Fields
    CREATED_BY = models.ForeignKey('self', on_delete=models.PROTECT,null=True, related_name='user_created', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_updated', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

   # Required for Django Auth
    USERNAME_FIELD = 'EMAIL'
    REQUIRED_FIELDS = ['USERNAME']
    
    class Meta:
        db_table = 'USERS'
        manage: True

    def __str__(self):
        return str(self.ID)
    
# --- Authentication Overrides ---

    @property
    def is_authenticated(self):
        """
        Always returns False to reject Django's default authentication 
        check for this model instance.
        """
        return False

    @property
    def is_anonymous(self):
        """
        Conversely, this should be True if is_authenticated is False.
        """
        return True

    def set_password(self, raw_password):
        self.PASSWORD_HASH = make_password(raw_password)
        self.PASSWORD_CHANGED_AT = timezone.now()

    def check_password(self, raw_password):
        return check_password(raw_password, self.PASSWORD_HASH)

class UserProfile(models.Model):
    USER_ID = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True,name="name_user_profile_id", db_column='USER_ID')
    NAME = models.CharField(max_length=100, db_column='NAME')
    NAME_ENGLISH = models.CharField(max_length=100, null=True, blank=True, db_column='NAME_ENGLISH')
    GENDER = models.CharField(max_length=20, null=True, blank=True, db_column='GENDER')
    DOB = models.DateField(null=True, blank=True, db_column='DOB')
    POB = models.TextField(null=True, blank=True, db_column='POB')
    MARITAL_STATUS = models.CharField(max_length=20, null=True, blank=True, db_column='MARITAL_STATUS')
    NATIONAL_ID = models.CharField(max_length=25, null=True, blank=True, db_column='NATIONAL_ID')
    NATIONALITY = models.CharField(max_length=100, null=True, blank=True, db_column='NATIONALITY')
    OCCUPATION = models.CharField(max_length=100, null=True, blank=True, db_column='OCCUPATION')

    COUNTRY_ID = models.ForeignKey('admin_address.Country', on_delete=models.PROTECT, default=1, db_column='COUNTRY_ID')
    PROVINCE_ID = models.ForeignKey('admin_address.Province', on_delete=models.SET_NULL, null=True, blank=True, db_column='PROVINCE_ID')
    DISTRICT_ID = models.ForeignKey('admin_address.District', on_delete=models.SET_NULL, null=True, blank=True, db_column='DISTRICT_ID')
    COMMUNE_ID = models.ForeignKey('admin_address.Commune', on_delete=models.SET_NULL, null=True, blank=True, db_column='COMMUNE_ID')
    VILLAGE_ID = models.ForeignKey('admin_address.Village', on_delete=models.SET_NULL, null=True, blank=True, db_column='VILLAGE_ID')


    ADDRESS_LINE1 = models.CharField(max_length=255, null=True, blank=True, db_column='ADDRESS_LINE1')
    ADDRESS_LINE2 = models.CharField(max_length=255, null=True, blank=True, db_column='ADDRESS_LINE2')
    ZIP_CODE = models.CharField(max_length=20, null=True, blank=True, db_column='ZIP_CODE')
    POSTAL_CODE = models.CharField(max_length=20, null=True, blank=True, db_column='POSTAL_CODE')

    PROFILE_PICTURE_URL = models.URLField(max_length=500, null=True, blank=True, db_column='PROFILE_PICTURE_URL')
    SIGNATURE_URL = models.URLField(max_length=500, null=True, blank=True, db_column='SIGNATURE_URL')
    BIO = models.TextField(null=True, blank=True, db_column='BIO')

    LANGUAGE_PREFERENCE = models.CharField(max_length=2, default='km', db_column='LANGUAGE_PREFERENCE')
    TIMEZONE = models.CharField(max_length=50, default='Asia/Phnom_Penh', db_column='TIMEZONE')
    IS_VERIFIED = models.BooleanField(default=False, db_column='IS_VERIFIED')

    FACEBOOK_LINK = models.URLField(max_length=255, null=True, blank=True, db_column='FACEBOOK_LINK')
    TIKTOK_LINK = models.URLField(max_length=255, null=True, blank=True, db_column='TIKTOK_LINK')
    LINKEDIN_LINK = models.URLField(max_length=255, null=True, blank=True, db_column='LINKEDIN_LINK')
    WEBSITE = models.URLField(max_length=255, null=True, blank=True, db_column='WEBSITE')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_user_profiles', db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name='updated_user_profiles', db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'USER_PROFILES'