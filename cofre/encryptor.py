from cryptography.fernet import Fernet
from decouple import config
from administration.models import Parametro  # Certifique-se de importar o modelo correto


def get_crypt_key():
    """
    Busca a chave de criptografia no banco de dados.
    Filtra pelo módulo 'cofre' e código 'chave_cofre'.
    """
    try:
        parametro = Parametro.objects.get(modulo='cofre', codigo='chave_cofre')
        return parametro.valor.encode()  # Retorna a chave como bytes
    except Parametro.DoesNotExist:
        raise ValueError("A chave de criptografia não foi encontrada no banco de dados.")

# Obtém a chave de criptografia
key = get_crypt_key()
cipher_suite = Fernet(key)

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