import os
import random
import sys

import pytest
from cryptography.fernet import InvalidToken

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.encryption import decrypt, encrypt


@pytest.fixture()
def master_key():
    return ''.join(random.sample(
        'abcdefghijklnopqrstuvwxyz',
        random.randint(3, 10)
    ))


@pytest.fixture()
def string_to_encrypt():
    return ''.join(random.sample(
        'abcdefghijklnopqrstuvwxyz',
        random.randint(3, 10)
    ))


@pytest.fixture()
def salt():
    return os.urandom(16)


def test_encryption_positive_case(master_key, string_to_encrypt, salt):
    encrypted, returned_salt = encrypt(master_key, string_to_encrypt, salt)
    decrypted = decrypt(master_key, encrypted, salt)

    assert isinstance(encrypted, bytes)
    assert returned_salt == salt
    assert decrypted == string_to_encrypt


def test_encryption_uniq_salt(master_key, string_to_encrypt):
    encrypted1, returned_salt1 = encrypt(master_key, string_to_encrypt)
    encrypted2, returned_salt2 = encrypt(master_key, string_to_encrypt)
    
    assert returned_salt1 != returned_salt2
    assert encrypted1 != encrypted2


def test_encryption_fixed_salt(master_key, string_to_encrypt, salt):
    encrypted1, returned_salt1 = encrypt(master_key, string_to_encrypt, salt)
    encrypted2, returned_salt2 = encrypt(master_key, string_to_encrypt, salt)

    assert returned_salt1 == returned_salt2
    assert encrypted1 != encrypted2
    

def test_encryption_default_string(master_key, salt):
    encrypted, _ = encrypt(master_key, salt=salt)
    decrypted = decrypt(master_key, encrypted, salt)
    
    assert decrypted == 'control'


def test_encryption_decrypt_with_wrong_mk(master_key, string_to_encrypt, salt):
    encrypted, _ = encrypt(master_key, string_to_encrypt, salt)
    wrong_mk = 'wrong_master_key'

    with pytest.raises(InvalidToken):
        decrypt(wrong_mk, encrypted, salt)


def test_encryption_decrypt_with_wrong_salt(
    master_key, string_to_encrypt, salt
):
    encrypted, _ = encrypt(master_key, string_to_encrypt, salt)
    wrong_salt = os.urandom(16)

    with pytest.raises(InvalidToken):
        decrypt(master_key, encrypted, wrong_salt)


def test_encryption_decrypt_tampered_encrypted(
    master_key, string_to_encrypt, salt
):
    encrypted, _ = encrypt(master_key, string_to_encrypt, salt)
    tampered = encrypted[:-1] + bytes([(encrypted[-1] + 1) % 256])

    with pytest.raises(InvalidToken):
        decrypt(master_key, tampered, salt)


def test_encryption_with_empty_string(master_key, salt):
    encrypted, _ = encrypt(master_key, '', salt)
    decrypted = decrypt(master_key, encrypted, salt)
    
    assert decrypted == ''


def test_encryption_with_empty_mk(string_to_encrypt, salt):
    encrypted, _ = encrypt('', string_to_encrypt, salt)
    decrypted = decrypt('', encrypted, salt)
    
    assert decrypted == string_to_encrypt