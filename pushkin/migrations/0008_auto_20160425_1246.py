# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0007_auto_20160425_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('command_group', models.ForeignKey(to='pushkin.CommandGroup')),
                ('device', models.ForeignKey(to='pushkin.Device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='service_device_commands',
            field=models.ManyToManyField(to='pushkin.CommandGroup', through='pushkin.Service'),
        ),
    ]
