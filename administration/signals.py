
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from administration.models import Parametro

@receiver(post_migrate)
def criar_parametros_padrao(sender, **kwargs):
    """
    Cria os parâmetros padrão após a execução das migrações.
    """
    # Verifica se o app é o "administration"
    if sender.name != "administration":
        return

    parametros_padrao = [
        {'modulo': 'suporte', 'codigo': 'idServidorFluig', 'tipo_dado': 'inteiro', 'valor': '1'},
        {'modulo': 'cofre', 'codigo': 'chave_cofre', 'tipo_dado': 'secret', 'valor': 'aaaaaaaa'},
        # Adicione outros parâmetros padrão aqui
    ]

    for parametro in parametros_padrao:
        # Usa get_or_create para evitar duplicação
        obj, created = Parametro.objects.get_or_create(
            modulo=parametro['modulo'],
            codigo=parametro['codigo'],
            defaults={
                'tipo_dado': parametro['tipo_dado'],
                'valor': parametro['valor'],
            }
        )
        if created:
            print(f"Parâmetro criado: {parametro['codigo']}")
        else:
            print(f"Parâmetro já existente: {parametro['codigo']}")