import secrets


def generate_salt(size=16):
    return secrets.token_bytes(size)
