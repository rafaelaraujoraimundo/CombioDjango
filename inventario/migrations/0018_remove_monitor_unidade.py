# Generated by Django 5.0.2 on 2024-10-25 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_monitor_estabelecimento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='unidade',
        ),
    ]
