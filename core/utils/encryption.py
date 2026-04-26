# utils/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings



# Generate once and store in settings (DO NOT regenerate each time)
# FERNET_KEY = b'your-fernet-key-32bytes.jurb564wq327qorfmjsdahdfafsdahfosdoak=='  # Must be 32 bytes base64-encoded
from decouple import config
# FERNET_KEY = config("FERNET_KEY")  # ✅ No casting
# FERNET_KEY = config("FERNET_KEY", cast=str)

fernet = settings.FERNET_KEY
# print(f"FERNET_KEY: {fernet}")  # Debugging line to check the key

fernet = Fernet(fernet)

def encrypt_text(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
