# Generated by Django 5.0.2 on 2024-07-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novosProjetos', '0002_projeto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='anexo_documentacao',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='anexo_escopo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='anexo_fontes',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
