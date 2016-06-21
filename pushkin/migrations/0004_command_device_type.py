# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0003_remove_command_device_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='device_type',
            field=models.ForeignKey(default=1, to='pushkin.DeviceType'),
            preserve_default=False,
        ),
    ]
