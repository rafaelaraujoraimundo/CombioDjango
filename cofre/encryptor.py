from cryptography.fernet import Fernet
from decouple import config


def encrypt_password(password: str, vault) -> str:
    """
    Criptografa a senha usando a chave associada ao Vault.
    """
    if not vault or not vault.valor:
        raise ValueError("Vault ou sua chave (valor) não podem ser None.")
    
    # Obtém a chave do Vault
    key = vault.valor.encode()
    cipher_suite = Fernet(key)
    
    # Criptografa a senha
    return cipher_suite.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password: str, vault) -> str:
    """
    Descriptografa a senha usando a chave associada ao Vault.
    """
    if not vault or not vault.valor:
        raise ValueError("Vault ou sua chave (valor) não podem ser None.")
    
    # Obtém a chave do Vault
    key = vault.valor.encode()
    cipher_suite = Fernet(key)
    
    # Descriptografa a senha
    return cipher_suite.decrypt(encrypted_password.encode()).decode()