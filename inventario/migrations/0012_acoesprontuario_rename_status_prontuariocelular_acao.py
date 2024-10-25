# Generated by Django 5.0.2 on 2024-10-25 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_rename_unidade_celular_estabelecimento'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcoesProntuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acao', models.CharField(max_length=100, unique=True)),
                ('tipo', models.IntegerField(choices=[(1, 'Manutenção'), (2, 'Transferência'), (3, 'Apontamento')])),
            ],
        ),
        migrations.RenameField(
            model_name='prontuariocelular',
            old_name='status',
            new_name='acao',
        ),
    ]
