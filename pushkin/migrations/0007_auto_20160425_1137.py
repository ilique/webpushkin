# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0006_auto_20160418_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='device_type',
        ),
        migrations.AddField(
            model_name='commandgroup',
            name='device_type',
            field=models.ForeignKey(default=0, to='pushkin.DeviceType'),
            preserve_default=False,
        ),
    ]
