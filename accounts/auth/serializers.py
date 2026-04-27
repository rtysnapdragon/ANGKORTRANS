from rest_framework import serializers
from .models import (
    User, Role, UserRole, Permission, RolePermission,
    RefreshToken, AuthAuditLog,
    UserOTP, LoginHistory,ForgotOrResetPassword
)
from accounts.users.models import UserProfile
from admin_address.models import Country, Province, District, Commune, Village


from rest_framework import serializers
from .models import User

class RefreshTokenResponseSerializer(serializers.Serializer):
    AccessToken = serializers.CharField()
    RefreshToken = serializers.CharField()
    
class LoginSerializer(serializers.Serializer):
    UsernameOrEmail = serializers.CharField()
    Password = serializers.CharField(write_only=True)
    
class RefreshTokenSerializer(serializers.Serializer):
    RefreshToken = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    Code = serializers.CharField()
    Username = serializers.CharField()
    Email = serializers.EmailField()
    Password = serializers.CharField(write_only=True)
    Name = serializers.CharField()

class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ['OtpCode', 'OtpType', 'ExpiresAt', 'IsUsed']
    OtpCode = serializers.CharField(source='OTP_CODE')
    OtpType = serializers.CharField(source='OTP_TYPE')
    ExpiresAt = serializers.DateTimeField(source='EXPIRES_AT')
    IsUsed = serializers.BooleanField(source='IS_USED')

class ForgotOrResetPasswordSerializer(serializers.Serializer):
    Token = serializers.CharField()
    NewPassword = serializers.CharField(min_length=6)
    ConfirmPassword = serializers.CharField(min_length=6)

    def validate(self, data):
        if data["NewPassword"] != data["ConfirmPassword"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
