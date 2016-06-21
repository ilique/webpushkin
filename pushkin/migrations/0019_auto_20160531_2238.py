# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0018_auto_20160531_2237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='command',
            old_name='group',
            new_name='command_group',
        ),
    ]
