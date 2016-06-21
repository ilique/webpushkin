# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pushkin', '0010_auto_20160425_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceSoftware',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='commandgroup',
            name='device_type',
            field=models.ForeignKey(to='pushkin.DeviceType', on_delete=django.db.models.deletion.SET_NULL, null=True,
                                    blank=True),
        ),
        migrations.AddField(
            model_name='commandgroup',
            name='device_model',
            field=models.ForeignKey(to='pushkin.DeviceModel', on_delete=django.db.models.deletion.SET_NULL, null=True,
                                    blank=True),
        ),
        migrations.AddField(
            model_name='commandgroup',
            name='device_software',
            field=models.ForeignKey(to='pushkin.DeviceSoftware', on_delete=django.db.models.deletion.SET_NULL,
                                    null=True, blank=True),
        ),
    ]
