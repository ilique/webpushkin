# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0009_auto_20160425_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='service_device_commands',
        ),
        migrations.RemoveField(
            model_name='service',
            name='command_group',
        ),
        migrations.RemoveField(
            model_name='service',
            name='device',
        ),
        migrations.AddField(
            model_name='commandgroup',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='pushkin.Service',
                                    null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='pushkin.Service',
                                    null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(default=0, to='pushkin.DeviceType'),
            preserve_default=False,
        ),
    ]
