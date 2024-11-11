import django.conf
from django.contrib import messages
import django.db
from django.utils import timezone
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
import logging
from django.db import transaction
from administration.views import User
from requests_oauthlib import OAuth1Session
from .models import UsuarioDesligamento, UsuarioFluig
from administration.models import ServidorFluig
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
import json

logger = logging.getLogger(__name__)

@shared_task
def verificar_bloqueios_pendentes():
    # Busca todos os registros que têm qualquer bloqueio como False
    registros_pendentes = UsuarioDesligamento.objects.filter(
        bloqueio_email=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_fluig=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_datasul=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_monday=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_qualiteam=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_portal_chamados=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_usuario_impressora=False
    )

    if registros_pendentes.exists():
        # Cria a tabela HTML com estilização de cores e coluna para data limite
        mensagem_html = """
        <p>Os seguintes usuários possuem sistemas pendentes de bloqueio:</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Usuário</th>
                <th>Data Limite</th>
                <th>Email</th>
                <th>Fluig</th>
                <th>Datasul</th>
                <th>Monday</th>
                <th>Qualiteam</th>
                <th>Portal de Chamados</th>
                <th>Usuário da Impressora (Matriz)</th>
            </tr>
        """
        
        for registro in registros_pendentes:
            mensagem_html += f"""
                <tr>
                    <td>{registro.usuario}</td>
                    <td>{registro.data_limite.strftime('%d/%m/%Y') if registro.data_limite else 'Não definida'}</td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_email else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_email else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_fluig else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_fluig else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_datasul else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_datasul else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_monday else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_monday else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_qualiteam else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_qualiteam else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_portal_chamados else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_portal_chamados else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_usuario_impressora else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_usuario_impressora else 'Bloqueado'}
                    </td>
                </tr>
            """
        usuarios = User.objects.filter(enviar_email_desligados=True)
        emails = [usuario.email for usuario in usuarios]
        mensagem_html += "</table>"

        # Envia o e-mail usando send_mail com o corpo em HTML
        send_mail(
            subject="Alerta: Bloqueios Pendentes de Usuários",
            message="Os seguintes usuários possuem sistemas pendentes de bloqueio. Confira o conteúdo em HTML para mais detalhes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            html_message=mensagem_html  # Define o corpo do e-mail em HTML
        )


@shared_task
def update_usuario_fluig():
    try:
        print("Iniciando atualização de usuários Fluig")
        servidor_fluig = ServidorFluig.objects.get(id=1)
        oauth = OAuth1Session(
            servidor_fluig.client_key,
            client_secret=servidor_fluig.consumer_secret,
            resource_owner_key=servidor_fluig.access_token,
            resource_owner_secret=servidor_fluig.access_secret
        )

        url = servidor_fluig.url + "/api/public/2.0/users/listAll?limit=800"
        response = oauth.get(url, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            data = response.json().get('content', [])
            with transaction.atomic():
                for user in data:
                    login = user.get("login")
                    email = user.get("email", "")
                    code = user.get("code", "")
                    full_name = user.get("fullName", "")
                    is_active = user.get("isActive", False)

                    # Update or create UsuarioFluig entry
                    UsuarioFluig.objects.update_or_create(
                        login=login,
                        defaults={
                            "email": email,
                            "code": code,
                            "full_name": full_name,
                            "is_active": is_active,
                        },
                    )
            print("Finalizando atualização de usuários Fluig")
        else:
            print(f"Falha ao buscar dados de usuários: {response.status_code} - {response.text}")
    except ServidorFluig.DoesNotExist:
        print("Servidor Fluig não configurado corretamente.")


@shared_task
def substituir_usuario_fluig(json_data):
    try:
        logger.info("Iniciando substituição de usuário no Fluig")
        
        # Obter credenciais do servidor Fluig
        servidor_fluig = ServidorFluig.objects.get(id=1)
        oauth = OAuth1Session(
            servidor_fluig.client_key,
            client_secret=servidor_fluig.consumer_secret,
            resource_owner_key=servidor_fluig.access_token,
            resource_owner_secret=servidor_fluig.access_secret
        )

        # URL para substituição de usuário
        url = servidor_fluig.url + "/api/public/bpm/substituteUser/create"
        headers = {'Content-Type': 'application/json'}

        # Executar a requisição POST para substituir usuário
        response = oauth.post(url, headers=headers, json=json_data)

        # Verificar resposta
        if response.status_code == 200:
            logger.info("Substituição de usuário realizada com sucesso.")
        else:
            logger.error(f"Falha na substituição de usuário: {response.status_code} - {response.text}")
            # Possível retorno de falha para tratamento na view ou log detalhado
            return {"status": "error", "message": f"Falha na substituição de usuário: {response.status_code} - {response.text}"}

    except ObjectDoesNotExist:
        logger.error("Servidor Fluig não configurado corretamente.")
        return {"status": "error", "message": "Servidor Fluig não configurado corretamente."}

    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar substituir o usuário: {e}")
        return {"status": "error", "message": f"Ocorreu um erro ao tentar substituir o usuário: {e}"}

    return {"status": "success", "message": "Substituição de usuário realizada com sucesso."}