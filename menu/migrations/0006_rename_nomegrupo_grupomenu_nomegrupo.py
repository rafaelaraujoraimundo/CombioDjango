# Generated by Django 5.0.2 on 2024-03-26 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_rename_nomegrupo_grupomenu_nomegrupo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grupomenu',
            old_name='NomeGrupo',
            new_name='nomegrupo',
        ),
    ]
