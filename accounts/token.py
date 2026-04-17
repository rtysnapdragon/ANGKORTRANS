from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from riththy_app.utils.encryption import encrypt_text

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims
        data['UserCode'] = self.user.CODE
        data['Username'] = self.user.USERNAME
        data['UserType'] = self.user.USER_TYPE
        data['Email'] = self.user.EMAIL
        data['Phone'] = self.user.PHONE_NUMBER

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom fields to the token payload
        token['UserId'] = encrypt_text(str(user.id))
        token['UserCode'] = user.CODE
        token['Username'] = user.USERNAME
        token['UserType'] = user.USER_TYPE
        token['Email'] = user.EMAIL

        # # Encrypt sensitive fields
        # token['user_id'] = encrypt_text(str(user.id))
        # token['CODE'] = encrypt_text(user.CODE)
        # token['username'] = encrypt_text(user.USERNAME)
        # token['user_type'] = encrypt_text(user.USER_TYPE)
        # token['email'] = encrypt_text(user.EMAIL)
        
        return token
