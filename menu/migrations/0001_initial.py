# Generated by Django 4.2 on 2023-05-22 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='codigo default', max_length=40)),
                ('NomeGrupo', models.CharField(max_length=40)),
                ('icon_grupo', models.CharField(max_length=80)),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.group')),
            ],
            options={
                'db_table': 'grupoMenu',
            },
        ),
        migrations.CreateModel(
            name='ItensMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='codigo default', max_length=40)),
                ('Item', models.CharField(max_length=40)),
                ('icon_item', models.CharField(max_length=80)),
                ('url', models.CharField(max_length=80)),
                ('grupo_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='menu.grupomenu')),
                ('permission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.permission')),
            ],
            options={
                'db_table': 'ItensMenu',
            },
        ),
    ]