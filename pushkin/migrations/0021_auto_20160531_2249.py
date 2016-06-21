# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0020_auto_20160531_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commandgroup',
            old_name='command',
            new_name='commands',
        ),
    ]
