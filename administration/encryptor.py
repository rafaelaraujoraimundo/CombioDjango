from cryptography.fernet import Fernet
from decouple import config
import os
# Usar a chave de ambiente
key = config('CRYPT_KEY').encode()
cipher_suite = Fernet(key)

def encrypt_password(password: str) -> str:
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return cipher_suite.decrypt(encrypted_password.encode()).decode()