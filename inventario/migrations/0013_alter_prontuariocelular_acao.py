# Generated by Django 5.0.2 on 2024-10-25 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_acoesprontuario_rename_status_prontuariocelular_acao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prontuariocelular',
            name='acao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.acoesprontuario'),
        ),
    ]
