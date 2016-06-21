# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0015_commandgroup_device_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandgroup',
            name='device_type',
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='type',
            field=models.ManyToManyField(to='pushkin.DeviceType'),
        ),
    ]
