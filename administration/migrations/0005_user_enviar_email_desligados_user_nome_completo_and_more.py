# Generated by Django 5.0.2 on 2024-11-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_passwordgroup_passwordtype_passwordmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enviar_email_desligados',
            field=models.BooleanField(default=False, verbose_name='Enviar e-mail de desligamento?'),
        ),
        migrations.AddField(
            model_name='user',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Usuário ativo?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Usuário é da equipe de desenvolvimento?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Usuário é um superusuário?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='usuario_datasul',
            field=models.CharField(max_length=50, verbose_name='Usuário Datasul'),
        ),
    ]
