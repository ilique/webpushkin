# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0013_auto_20160524_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandgroup',
            name='device_type',
        ),
    ]
