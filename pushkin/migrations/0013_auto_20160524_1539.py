# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0012_auto_20160524_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='service',
        ),
        migrations.RemoveField(
            model_name='device',
            name='type',
        ),
        migrations.AlterField(
            model_name='commandgroup',
            name='device_model',
            field=models.ForeignKey(to='pushkin.DeviceModel', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commandgroup',
            name='device_type',
            field=models.ForeignKey(to='pushkin.DeviceType', blank=True, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.DeleteModel(
            name='Device',
        ),
    ]
