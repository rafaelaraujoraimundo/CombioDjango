# Generated by Django 5.0.2 on 2024-11-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cofre', '0003_passwordmanager_usuario_criacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vault',
            name='valor',
            field=models.CharField(max_length=44, verbose_name='Chave de Criptografia'),
        ),
    ]
