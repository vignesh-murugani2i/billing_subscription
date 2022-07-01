"""used to encrypt and decrypt a string using salt
"""
import os

import base64
import logging
import traceback

from cryptography.fernet import Fernet

logger = logging.getLogger('root')


def encrypt(password, salt):
    """used to encrypt given value with salt
    """
    try:
        password = str(password)
        cipher_pass = Fernet(salt)
        encrypt_pass = cipher_pass.encrypt(password.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass

    except Exception as e:
        return None


def decrypt(password, salt):
    """used to decrypt given value with salt
    """
    try:
        password = base64.urlsafe_b64decode(password)
        cipher_pass = Fernet(salt)
        decode_pass = cipher_pass.decrypt(password).decode("ascii")
        return decode_pass
    except Exception as e:
        return None


def generate_key():
    """used to generate random 32 character byte code
    that can be used as salt value
    """
    return base64.urlsafe_b64encode(os.urandom(32))
