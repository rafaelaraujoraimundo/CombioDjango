# Generated by Django 5.0.2 on 2025-05-30 15:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suporte', '0006_usuariodesligamento_backup_desktop_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MS365Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_empresa', models.CharField(help_text='Nome identificador da empresa/tenant', max_length=200, verbose_name='Nome da Empresa')),
                ('tenant_id', models.CharField(help_text='ID do tenant no Azure AD', max_length=100, verbose_name='Tenant ID')),
                ('client_id', models.CharField(help_text='Application (client) ID do app registration', max_length=100, verbose_name='Client ID')),
                ('encrypted_client_secret', models.TextField(help_text='Client secret criptografado', verbose_name='Client Secret')),
                ('ativo', models.BooleanField(default=True, help_text='Se este tenant está ativo para uso', verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Criação')),
                ('data_ultima_alteracao', models.DateTimeField(auto_now=True, verbose_name='Última Alteração')),
                ('observacoes', models.TextField(blank=True, help_text='Observações sobre este tenant', null=True, verbose_name='Observações')),
                ('usuario_criacao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='m365_tenants_criados', to=settings.AUTH_USER_MODEL, verbose_name='Usuário de Criação')),
                ('usuario_ultima_alteracao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='m365_tenants_alterados', to=settings.AUTH_USER_MODEL, verbose_name='Último Usuário que Alterou')),
            ],
            options={
                'verbose_name': 'Tenant Microsoft 365',
                'verbose_name_plural': 'Tenants Microsoft 365',
                'ordering': ['nome_empresa'],
            },
        ),
        migrations.CreateModel(
            name='MS365UserSearchLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termo_busca', models.CharField(help_text='Email ou ID do usuário pesquisado', max_length=255, verbose_name='Termo de Busca')),
                ('encontrado', models.BooleanField(default=False, verbose_name='Usuário Encontrado')),
                ('dados_encontrados', models.JSONField(blank=True, help_text='Dados do usuário encontrado (sem informações sensíveis)', null=True, verbose_name='Dados Encontrados')),
                ('data_pesquisa', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data da Pesquisa')),
                ('ip_origem', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP de Origem')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suporte.ms365tenant', verbose_name='Tenant')),
                ('usuario_pesquisador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário que Pesquisou')),
            ],
            options={
                'verbose_name': 'Log de Busca M365',
                'verbose_name_plural': 'Logs de Busca M365',
                'ordering': ['-data_pesquisa'],
            },
        ),
        migrations.CreateModel(
            name='MS365UserUpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_alvo', models.CharField(help_text='Email ou ID do usuário que foi atualizado', max_length=255, verbose_name='Usuário Alvo')),
                ('campos_atualizados', models.JSONField(help_text='Campos que foram alterados e seus novos valores', verbose_name='Campos Atualizados')),
                ('sucesso', models.BooleanField(default=False, verbose_name='Atualização Bem-sucedida')),
                ('erro_detalhes', models.TextField(blank=True, help_text='Detalhes do erro caso a atualização tenha falhado', null=True, verbose_name='Detalhes do Erro')),
                ('data_atualizacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data da Atualização')),
                ('ip_origem', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP de Origem')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suporte.ms365tenant', verbose_name='Tenant')),
                ('usuario_atualizador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário que Atualizou')),
            ],
            options={
                'verbose_name': 'Log de Atualização M365',
                'verbose_name_plural': 'Logs de Atualização M365',
                'ordering': ['-data_atualizacao'],
            },
        ),
    ]
