# Generated by Django 5.0.2 on 2024-10-25 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0013_alter_prontuariocelular_acao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prontuariomonitor',
            old_name='local_destino',
            new_name='local',
        ),
        migrations.RemoveField(
            model_name='prontuariomonitor',
            name='observacao',
        ),
        migrations.RemoveField(
            model_name='prontuariomonitor',
            name='status',
        ),
        migrations.AddField(
            model_name='prontuariomonitor',
            name='acao',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='inventario.acoesprontuario'),
            preserve_default=False,
        ),
    ]
