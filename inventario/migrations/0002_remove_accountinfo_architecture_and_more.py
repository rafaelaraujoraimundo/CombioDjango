# Generated by Django 5.0.2 on 2024-10-17 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountinfo',
            name='architecture',
        ),
        migrations.RemoveField(
            model_name='accountinfo',
            name='bitswidth',
        ),
        migrations.RemoveField(
            model_name='accountinfo',
            name='install_date',
        ),
        migrations.RemoveField(
            model_name='accountinfo',
            name='publisher_id',
        ),
        migrations.RemoveField(
            model_name='accountinfo',
            name='version_id',
        ),
        migrations.RemoveField(
            model_name='bios',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='bios',
            name='name',
        ),
        migrations.RemoveField(
            model_name='bios',
            name='version',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='clock_speed',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='name',
        ),
        migrations.RemoveField(
            model_name='memory',
            name='size',
        ),
        migrations.RemoveField(
            model_name='software',
            name='name',
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_14',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_4',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_5',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_7',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_8',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='fields_9',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='tag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='asset_tag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='bdate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='bmanufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='bversion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='mmanufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='mmodel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='msn',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='smanufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='smodel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='ssn',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bios',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cores',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='cpu_arch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='current_address_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='current_speed',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='data_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='l2_cache_size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='logical_cpus',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='socket',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='speed',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='voltage',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='arch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='archive',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='category_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='checksum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='default_gateway',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='device_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='dns',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='etime',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='fidelity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='ipaddr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='ipsrc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='last_come',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='last_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='memory',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='os_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='os_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='os_version',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='processor_n',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='processor_t',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='processors',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='quality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='sstate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='swap',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='user_domain',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='user_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='uuid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='win_company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='win_owner',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='win_prod_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='win_prod_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='workgroup',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='caption',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='num_slots',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='purpose',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='memory',
            name='speed',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='architecture',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='bitswidth',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='filesize',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='folder',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='guid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='name_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='source',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountinfo', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='bios',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bios', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpus', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memories', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='software',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='software', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='software',
            name='publisher_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='software',
            name='version_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='disk_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='firmware',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='hardware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storages', to='inventario.hardware'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]