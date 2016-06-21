# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0014_remove_commandgroup_device_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandgroup',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='pushkin.DeviceType', null=True,
                                    blank=True),
        ),
    ]
