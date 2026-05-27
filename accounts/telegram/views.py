from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from accounts.telegram.models import (
    UserTelegram
)

from accounts.telegram.serializers import (
    UserTelegramSerializer
)

from core.utils.telegram import (
    verify_telegram_auth
)
# def check_telegram_data(data: dict) -> bool:
#     token = settings.TELEGRAM_BOT_TOKEN
#     secret = hashlib.sha256(token.encode()).digest()

#     hash_value = data.pop('hash', None)
#     if not hash_value:
#         return False

#     data_check_string = '\n'.join(
#         f"{k}={v}" for k, v in sorted(data.items())
#     )

#     calculated_hash = hmac.new(
#         secret, data_check_string.encode(), hashlib.sha256
#     ).hexdigest()

#     return hmac.compare_digest(calculated_hash, hash_value)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def telegram_login_view(request):

    data = request.data.copy()

    if not verify_telegram_auth(data):

        return Response(
            {
                'Success': False,
                'Message': 'Invalid Telegram authentication'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    telegram_id = data.get('id')

    user, created = (
        UserTelegram.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'telegram_username': data.get(
                    'username',
                    ''
                ),
                'avatar': data.get(
                    'photo_url',
                    ''
                ),
                'first_name': data.get(
                    'first_name',
                    ''
                ),
                'last_name': data.get(
                    'last_name',
                    ''
                ),
                'auth_date': data.get(
                    'auth_date'
                )
            }
        )
    )

    if not created:

        user.telegram_username = data.get(
            'username',
            ''
        )

        user.avatar = data.get(
            'photo_url',
            ''
        )

        user.first_name = data.get(
            'first_name',
            ''
        )

        user.last_name = data.get(
            'last_name',
            ''
        )

        user.auth_date = data.get(
            'auth_date'
        )

        user.save()

    refresh = RefreshToken()

    refresh['TelegramId'] = (
        user.telegram_id
    )

    refresh['Username'] = (
        user.telegram_username
    )

    serializer = (
        UserTelegramSerializer(user)
    )

    return Response(
        {
            'Success': True,
            'Message': 'Telegram login successful',
            'AccessToken': str(
                refresh.access_token
            ),
            'RefreshToken': str(refresh),
            'User': serializer.data
        },
        status=status.HTTP_200_OK
    )