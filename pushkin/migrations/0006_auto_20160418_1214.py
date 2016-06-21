# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0005_authparam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authparam',
            name='port',
            field=models.IntegerField(),
        ),
    ]
