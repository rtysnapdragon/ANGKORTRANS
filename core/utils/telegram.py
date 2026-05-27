import hashlib
import hmac

from django.conf import settings


def verify_telegram_auth(data):

    received_hash = data.get('hash')

    if not received_hash:
        return False

    auth_data = {
        key: value
        for key, value in data.items()
        if key != 'hash'
    }

    data_check_string = '\n'.join(
        sorted(
            f'{key}={value}'
            for key, value in auth_data.items()
        )
    )

    secret_key = hashlib.sha256(
        settings.TELEGRAM_BOT_TOKEN.encode()
    ).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        calculated_hash,
        received_hash
    )