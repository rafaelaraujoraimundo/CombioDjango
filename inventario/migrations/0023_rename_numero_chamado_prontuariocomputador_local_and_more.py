# Generated by Django 5.0.2 on 2024-10-28 17:13

import django.db.models.deletion
import inventario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0022_rename_departamento_computador_estabelecimento_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prontuariocomputador',
            old_name='numero_chamado',
            new_name='local',
        ),
        migrations.RenameField(
            model_name='prontuariocomputador',
            old_name='tipo_ocorrencia',
            new_name='unidade_destino',
        ),
        migrations.RemoveField(
            model_name='prontuariocomputador',
            name='observacao',
        ),
        migrations.AddField(
            model_name='computador',
            name='arquivo_computador',
            field=models.FileField(blank=True, null=True, upload_to=inventario.models.upload_to),
        ),
        migrations.AddField(
            model_name='prontuariocomputador',
            name='acao',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='inventario.acoesprontuario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prontuariocomputador',
            name='motivo_ocorrencia',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prontuariocomputador',
            name='usuario',
            field=models.CharField(default='rara', max_length=100),
            preserve_default=False,
        ),
    ]
