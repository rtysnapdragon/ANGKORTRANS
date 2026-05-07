from rest_framework import serializers
from accounts.users.models import Users as User
from django.contrib.auth.hashers import make_password, check_password

class SignupSerializer(serializers.ModelSerializer):
    Password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['CODE', 'NAME', 'USERNAME', 'EMAIL', 'PASSWORD', 'USER_TYPE', 'PHONE_NUMBER']

    def validate(self, data):
        if User.objects.filter(EMAIL=data['EMAIL']).exists():
            raise serializers.ValidationError("Email already exists.")
        if User.objects.filter(USERNAME=data['USERNAME']).exists():
            raise serializers.ValidationError("Username already exists.")
        return data

    def create(self, validated_data):
        password = make_password(validated_data.pop('PASSWORD'))
        user = User.objects.create(PASSWORD=password, **validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("Username")
        password = data.get("Password")
        try:
            user = User.objects.get(USERNAME=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.PASSWORD):
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user
        return data
