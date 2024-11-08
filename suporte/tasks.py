import django.conf
from django.utils import timezone
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
import logging
from administration.views import User
from .models import UsuarioDesligamento
from decouple import config
from django.core.mail import send_mail
from django.conf import settings

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
        # Cria a tabela HTML com estilização de cores
        mensagem_html = """
        <p>Os seguintes usuários possuem sistemas pendentes de bloqueio:</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Usuário</th>
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