import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.conf import settings

# Your secret key (must be same as frontend's SECRET_KEY)
# SECRET_KEY = 'shrshrefgsm5tw45t43yu56jhrtsgrdsg'
SECRET_KEY = settings.SECRET_KEY


def get_key_and_iv(password, salt, key_length=32, iv_length=16):
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def decrypt_cryptojs(encrypted, password=SECRET_KEY):
    encrypted_bytes = base64.b64decode(encrypted)
    if encrypted_bytes[:8] != b'Salted__':
        raise ValueError("Missing Salted__ prefix")
    salt = encrypted_bytes[8:16]
    encrypted_data = encrypted_bytes[16:]

    # Derive key and IV from password and salt
    key, iv = get_key_and_iv(password.encode('utf-8'), salt, 32, 16)

    # Create AES cipher with key and IV in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')
