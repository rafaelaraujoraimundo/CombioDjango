# Generated by Django 5.0.2 on 2024-07-26 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='whatsappmessage',
            old_name='timestamp',
            new_name='timestamp_recebido',
        ),
    ]