# suporte/m365_service.py - Novo arquivo

import requests
import logging
from typing import Dict, List, Optional, Tuple
from .models import MS365Tenant, MS365UserSearchLog, MS365UserUpdateLog

logger = logging.getLogger(__name__)


class MS365ApiService:
    """Serviço para interação com Microsoft Graph API"""
    
    def __init__(self, tenant: MS365Tenant):
        self.tenant = tenant
        self.access_token = None
        self.base_url = "https://graph.microsoft.com/V1.0"
    
    def authenticate(self) -> Tuple[bool, str]:
        """
        Autentica com Microsoft Graph API usando client credentials
        Returns: (success: bool, error_message: str)
        """
        auth_url = f"https://login.microsoftonline.com/{self.tenant.tenant_id}/oauth2/v2.0/token"
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.tenant.client_id,
            'client_secret': self.tenant.get_client_secret(),
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        try:
            response = requests.post(auth_url, headers=headers, data=data, timeout=30)

            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            if self.access_token:
                return True, ""
            else:
                return False, "Token de acesso não encontrado na resposta"
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout na autenticação com Microsoft Graph"
            logger.error(error_msg)
            return False, error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na autenticação: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _get_headers(self, include_consistency=False) -> Dict[str, str]:
        headers = {
        'Authorization': f'Bearer {self.access_token}',
        'Content-Type': 'application/json'
                    }
        if include_consistency:
            headers['ConsistencyLevel'] = 'eventual'
        return headers
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Testa a conexão com Microsoft Graph
        Returns: (success: bool, message: str)
        """
        # Primeiro autentica
        auth_success, auth_error = self.authenticate()
        if not auth_success:
            return False, f"Falha na autenticação: {auth_error}"
        
        # Tenta fazer uma chamada simples à API
        try:
            url = f"{self.base_url}/organization"
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                return True, "Conexão testada com sucesso!"
            else:
                return False, f"Erro na API: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Erro ao testar conexão: {str(e)}"
    
    def get_user(self, user_id: str, requesting_user=None, ip_address=None) -> Tuple[Optional[Dict], str]:
        """
        Busca informações de um usuário
        Returns: (user_data: Dict or None, error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return None, f"Falha na autenticação: {auth_error}"
        
        url = f"{self.base_url}/users/{user_id}?$select=id,displayName,givenName,surname,jobTitle,department,mail,userPrincipalName,MobilePhone,businessPhones,officeLocation,userType,accountEnabled,createdDateTime,preferredLanguage"
        print('url: '+ url)
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            print('response: '+ response.text)
            if response.status_code == 200:
                user_data = response.json()
                
                # Log da busca bem-sucedida
                self._log_search(user_id, True, user_data, requesting_user, ip_address)
                
                return user_data, ""
            
            elif response.status_code == 404:
                # Log da busca sem resultado
                self._log_search(user_id, False, None, requesting_user, ip_address)
                return None, "Usuário não encontrado"
            
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                self._log_search(user_id, False, None, requesting_user, ip_address)
                return None, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            self._log_search(user_id, False, None, requesting_user, ip_address)
            return None, error_msg
    
    def list_users(self, filter_str: str = None) -> Tuple[List[Dict], str]:
        """
        Lista todos os usuários do tenant, seguindo o @odata.nextLink se necessário.
        Returns: (users_list: List[Dict], error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return [], f"Falha na autenticação: {auth_error}"

        base_url = f"{self.base_url}/users"
        fields = (
            "id,displayName,givenName,surname,jobTitle,department,mail,userPrincipalName,"
            "mobilePhone,businessPhones,officeLocation,userType,accountEnabled,"
            "createdDateTime,preferredLanguage,signInActivity"
        )
        url = f"{base_url}?$select={fields}"

        if filter_str:
            url += f'&$search="displayName:{filter_str}"'

        headers = self._get_headers(include_consistency=bool(filter_str))

        all_users = []

        try:
            while url:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()

                data = response.json()
                users = data.get('value', [])
                all_users.extend(users)

                # Verifica se há próxima página
                url = data.get('@odata.nextLink')  # None encerra o loop

            return all_users, ""

        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao listar usuários: {str(e)}"
            logger.error(error_msg)
            return [], error_msg

    
    def update_user_profile(self, user_id: str, updates: Dict, requesting_user=None, ip_address=None) -> Tuple[bool, str]:
        """
        Atualiza dados do perfil do usuário
        Returns: (success: bool, error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return False, f"Falha na autenticação: {auth_error}"
        
        url = f"{self.base_url}/users/{user_id}"
        
        try:
            response = requests.patch(url, headers=self._get_headers(), json=updates, timeout=30)
            print(updates)
            if response.status_code == 204:  # No Content - sucesso
                # Log da atualização bem-sucedida
                self._log_update(user_id, updates, True, None, requesting_user, ip_address)
                return True, "Usuário atualizado com sucesso"
            
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                self._log_update(user_id, updates, False, error_msg, requesting_user, ip_address)
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            self._log_update(user_id, updates, False, error_msg, requesting_user, ip_address)
            return False, error_msg
    
    def get_user_manager(self, user_id: str) -> Tuple[Optional[Dict], str]:
        """
        Busca o manager de um usuário
        Returns: (manager_data: Dict or None, error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return None, f"Falha na autenticação: {auth_error}"
        
        url = f"{self.base_url}/users/{user_id}/manager"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                return response.json(), ""
            elif response.status_code == 404:
                return None, "Manager não encontrado"
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                return None, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            return None, error_msg
    
    def set_user_manager(self, user_id: str, manager_id: str) -> Tuple[bool, str]:
        """
        Define o manager de um usuário
        Returns: (success: bool, error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return False, f"Falha na autenticação: {auth_error}"
        
        url = f"{self.base_url}/users/{user_id}/manager/$ref"
        manager_url = f"{self.base_url}/users/{manager_id}"
        data = {"@odata.id": manager_url}
        
        try:
            response = requests.put(url, headers=self._get_headers(), json=data, timeout=30)
            
            if response.status_code == 204:  # No Content - sucesso
                return True, "Manager definido com sucesso"
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            return False, error_msg
    
    def remove_user_manager(self, user_id: str) -> Tuple[bool, str]:
        """
        Remove o manager de um usuário
        Returns: (success: bool, error_message: str)
        """
        if not self.access_token:
            auth_success, auth_error = self.authenticate()
            if not auth_success:
                return False, f"Falha na autenticação: {auth_error}"
        
        url = f"{self.base_url}/users/{user_id}/manager/$ref"
        
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 204:  # No Content - sucesso
                return True, "Manager removido com sucesso"
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            return False, error_msg
    
    def _log_search(self, termo_busca: str, encontrado: bool, dados_encontrados: Dict, requesting_user, ip_address):
        """Log interno para buscas"""
        try:
            # Remover dados sensíveis do log
            dados_log = None
            if dados_encontrados:
                dados_log = {
                    'displayName': dados_encontrados.get('displayName'),
                    'mail': dados_encontrados.get('mail'),
                    'userPrincipalName': dados_encontrados.get('userPrincipalName'),
                    'jobTitle': dados_encontrados.get('jobTitle'),
                    'department': dados_encontrados.get('department')
                }
            
            MS365UserSearchLog.objects.create(
                tenant=self.tenant,
                usuario_pesquisador=requesting_user,
                termo_busca=termo_busca,
                encontrado=encontrado,
                dados_encontrados=dados_log,
                ip_origem=ip_address
            )
        except Exception as e:
            logger.error(f"Erro ao salvar log de busca: {e}")
    
    def _log_update(self, usuario_alvo: str, campos_atualizados: Dict, sucesso: bool, erro_detalhes: str, requesting_user, ip_address):
        """Log interno para atualizações"""
        try:
            MS365UserUpdateLog.objects.create(
                tenant=self.tenant,
                usuario_atualizador=requesting_user,
                usuario_alvo=usuario_alvo,
                campos_atualizados=campos_atualizados,
                sucesso=sucesso,
                erro_detalhes=erro_detalhes,
                ip_origem=ip_address
            )
        except Exception as e:
            logger.error(f"Erro ao salvar log de atualização: {e}")