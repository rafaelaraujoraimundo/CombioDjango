# Generated by Django 5.0.2 on 2024-03-26 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0008_rename_journalingadherencefull_dataset_journalingadherencefull'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='journalingadherenceHalf',
            new_name='journalingadherencehalf',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='journalingadherenceNone',
            new_name='journalingadherencenone',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='syncstatusauccess',
            new_name='syncstatusasuccess',
        ),
    ]
