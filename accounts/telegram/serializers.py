# from rest_framework import serializers

from accounts.telegram.models import UserTelegram
from core.serializers import PascalCaseSerializer

class UserTelegramSerializer(
    PascalCaseSerializer
):
    class Meta:
        model = UserTelegram

        fields = '__all__'

# class UserTelegramSerializer(serializers.ModelSerializer):

#     Id = serializers.IntegerField(
#         source='id'
#     )

#     TelegramId = serializers.IntegerField(
#         source='telegram_id'
#     )

#     TelegramUsername = serializers.CharField(
#         source='telegram_username'
#     )

#     Avatar = serializers.CharField(
#         source='avatar'
#     )

#     FirstName = serializers.CharField(
#         source='first_name'
#     )

#     LastName = serializers.CharField(
#         source='last_name'
#     )

#     PhoneNumber = serializers.CharField(
#         source='phone_number'
#     )

#     Email = serializers.CharField(
#         source='email'
#     )

#     JoinedAt = serializers.DateTimeField(
#         source='joined_at'
#     )

#     CreatedAt = serializers.DateTimeField(
#         source='created_at'
#     )

#     UpdatedAt = serializers.DateTimeField(
#         source='updated_at'
#     )

#     class Meta:
#         model = UserTelegram

#         fields = [
#             'Id',
#             'TelegramId',
#             'TelegramUsername',
#             'Avatar',
#             'FirstName',
#             'LastName',
#             'PhoneNumber',
#             'Email',
#             'JoinedAt',
#             'CreatedAt',
#             'UpdatedAt',
#         ]