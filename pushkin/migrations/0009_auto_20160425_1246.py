# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0008_auto_20160425_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]
