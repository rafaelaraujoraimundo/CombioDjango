# Generated by Django 4.2.9 on 2024-02-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServidorFluig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servidor', models.CharField(max_length=255)),
                ('nome_servidor', models.CharField(max_length=255)),
                ('client_key', models.CharField(max_length=255)),
                ('consumer_secret', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=255)),
                ('access_secret', models.CharField(max_length=255)),
            ],
        ),
    ]