from celery import shared_task
from django.db import transaction
from requests_oauthlib import OAuth1Session
from .models import Process, ServidorFluig


@shared_task
def update_processes():
    try:
        print('Iniciando update_processes')
        servidor_fluig = ServidorFluig.objects.get(id=1)
        oauth = OAuth1Session(
            servidor_fluig.client_key,
            client_secret=servidor_fluig.consumer_secret,
            resource_owner_key=servidor_fluig.access_token,
            resource_owner_secret=servidor_fluig.access_secret
        )
        response = oauth.get(servidor_fluig.url + '/process-management/api/v2/processes', headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            data = response.json().get('items', [])
            with transaction.atomic():
                for item in data:
                    process_id = item.get('processId')
                    description = item.get('processDescription', '')
                    active = item.get('active', False)

                    # Atualiza o processo se ele existir ou cria um novo
                    Process.objects.update_or_create(
                        process_id=process_id,
                        defaults={'description': description, 'active': active}
                    )
            print('Finalizando update_processes')
    except ServidorFluig.DoesNotExist:
        print("Servidor Fluig não configurado corretamente.")