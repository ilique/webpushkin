# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0017_auto_20160531_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandgroup',
            name='command',
        ),
        migrations.AddField(
            model_name='command',
            name='group',
            field=models.ManyToManyField(to='pushkin.CommandGroup'),
        ),
    ]
