import base64
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(master_key, value_to_encrypt='control', salt=None):
    if not salt:
        salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    encrypted_value = f.encrypt(value_to_encrypt.encode())
    return encrypted_value, salt


def decrypt(master_key, encrypted_value, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    f = Fernet(key)
    return f.decrypt(encrypted_value).decode()