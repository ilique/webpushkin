# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0024_authparam_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='arguments',
            field=models.ManyToManyField(blank=True, null=True, to='pushkin.CommandArgument'),
        ),
    ]
