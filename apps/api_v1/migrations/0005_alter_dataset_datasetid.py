# Generated by Django 5.0.2 on 2024-03-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0004_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='datasetId',
            field=models.CharField(max_length=255),
        ),
    ]