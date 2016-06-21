# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0016_auto_20160525_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='command_group',
        ),
        migrations.AddField(
            model_name='commandgroup',
            name='command',
            field=models.ManyToManyField(to='pushkin.Command'),
        ),
    ]
