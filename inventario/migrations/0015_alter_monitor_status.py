# Generated by Django 5.0.2 on 2024-10-25 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0014_rename_local_destino_prontuariomonitor_local_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.status'),
        ),
    ]
