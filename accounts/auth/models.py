from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings
from accounts.users.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Role(models.Model):
    ID = models.AutoField(primary_key=True)
    CODE = models.CharField(max_length=50, unique=True)
    NAME = models.CharField(max_length=100, db_column='ROLE_NAME')
    DESCRIPTION = models.TextField(null=True, blank=True)

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="role_created_by")
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="role_updated_by")
    UPDATED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ROLES'


class UserRole(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="userrole_user_id", db_column='USER_ID')
    ROLE_ID = models.ForeignKey(Role, on_delete=models.CASCADE,related_name="userrole_role_id", db_column='ROLE_ID')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="userrole_created_by", db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="userrole_updated_by", db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'USER_ROLES'
        unique_together = ('USER_ID', 'ROLE_ID')


class Permission(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    CODE = models.CharField(max_length=100, unique=True, db_column='PERMISSION_CODE')
    NAME = models.CharField(max_length=150, db_column='PERMISSION_NAME')
    DESCRIPTION = models.TextField(null=True, blank=True, db_column='DESCRIPTION')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="permission_created_by", db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="permission_updated_by", db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'PERMISSIONS'


class RolePermission(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    ROLE_ID = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='ROLE_ID')
    PERMISSION_ID = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='PERMISSION_ID')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="rolepermission_created_by", db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="rolepermission_updated_by", db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'ROLE_PERMISSIONS'
        unique_together = ('ROLE_ID', 'PERMISSION_ID')


class RefreshToken(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='USER_ID')
    TOKEN_HASH = models.CharField(max_length=512, db_column='TOKEN_HASH')
    USER_AGENT = models.CharField(max_length=500, null=True, blank=True, db_column='USER_AGENT')
    IP_ADDRESS = models.GenericIPAddressField(null=True, blank=True, db_column='IP_ADDRESS')
    EXPIRES_AT = models.DateTimeField(db_column='EXPIRES_AT')
    IS_REVOKED = models.BooleanField(default=False, db_column='IS_REVOKED')
    REVOKED_AT = models.DateTimeField(null=True, blank=True, db_column='REVOKED_AT')

    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name="refreshtoken_created_by", db_column='CREATED_BY')
    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    UPDATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="refreshtoken_updated_by", db_column='UPDATED_BY')
    UPDATED_AT = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    class Meta:
        db_table = 'REFRESH_TOKENS'

class AuthAuditLog(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,related_name='authauditlog_user', db_column='USER_ID')
    EVENT_TYPE = models.CharField(max_length=50, db_column='EVENT_TYPE')  # LOGIN, LOGIN_FAILED, etc.
    EVENT_DESCRIPTION = models.TextField(null=True, blank=True, db_column='EVENT_DESCRIPTION')
    IP_ADDRESS = models.GenericIPAddressField(null=True, blank=True, db_column='IP_ADDRESS')
    USER_AGENT = models.CharField(max_length=500, null=True, blank=True, db_column='USER_AGENT')
    SUCCESS = models.BooleanField(default=True, db_column='SUCCESS')

    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,related_name='authauditlog_updated', db_column='CREATED_BY')

    class Meta:
        db_table = 'AUTH_AUDIT_LOG'
        
        
class ForgotOrResetPassword(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='password_reset_tokens', db_column='USER_ID')
    TOKEN_HASH = models.CharField(max_length=255, db_column='TOKEN_HASH')
    EXPIRES_AT = models.DateTimeField(db_column='EXPIRES_AT')
    IS_USED = models.BooleanField(default=False, db_column='IS_USED')

    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    CREATED_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='created_password_reset_tokens', db_column='CREATED_BY')

    class Meta:
        db_table = 'PASSWORD_RESET_TOKENS'
        
class UserOTP(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_otps', db_column='USER_ID')
    OTP_CODE = models.CharField(max_length=10, db_column='OTP_CODE')   # Store hashed in production
    OTP_TYPE = models.CharField(max_length=30, db_column='OTP_TYPE')
    EXPIRES_AT = models.DateTimeField(db_column='EXPIRES_AT')
    IS_USED = models.BooleanField(default=False, db_column='IS_USED')
    ATTEMPTS = models.IntegerField(default=0, db_column='ATTEMPTS')
    MAX_ATTEMPTS = models.IntegerField(default=5, db_column='MAX_ATTEMPTS')

    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    class Meta:
        db_table = 'USER_OTP'

class LoginHistory(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='USER_ID')
    LOGIN_TIME = models.DateTimeField(auto_now_add=True, db_column='LOGIN_TIME')
    LOGOUT_TIME = models.DateTimeField(null=True, blank=True, db_column='LOGOUT_TIME')
    IP_ADDRESS = models.GenericIPAddressField(null=True, blank=True, db_column='IP_ADDRESS')
    USER_AGENT = models.TextField(null=True, blank=True, db_column='USER_AGENT')
    LOGIN_STATUS = models.CharField(max_length=10, db_column='LOGIN_STATUS')
    FAILURE_REASON = models.CharField(max_length=255, null=True, blank=True, db_column='FAILURE_REASON')
    DEVICE_TYPE = models.CharField(max_length=50, null=True, blank=True, db_column='DEVICE_TYPE')
    BROWSER = models.CharField(max_length=50, null=True, blank=True, db_column='BROWSER')
    OS = models.CharField(max_length=50, null=True, blank=True, db_column='OS')

    CREATED_AT = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    class Meta:
        db_table = 'LOGIN_HISTORY'