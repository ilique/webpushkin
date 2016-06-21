# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0004_command_device_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol', models.CharField(max_length=255)),
                ('port', models.IntegerField(max_length=65535)),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
