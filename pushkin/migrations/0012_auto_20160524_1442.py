# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0011_auto_20160524_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='instructions',
            field=models.TextField(default='set of strings'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commandgroup',
            name='device_type',
            field=models.ForeignKey(default=5, to='pushkin.DeviceType'),
            preserve_default=False,
        ),
    ]
