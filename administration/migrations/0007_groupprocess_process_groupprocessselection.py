# Generated by Django 5.0.2 on 2024-11-08 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0006_user_hash_gravatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_id', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GroupProcessSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='process_selections', to='administration.groupprocess')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administration.process')),
            ],
            options={
                'unique_together': {('group', 'process')},
            },
        ),
    ]