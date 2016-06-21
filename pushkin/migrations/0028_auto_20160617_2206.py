# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 22:06
from __future__ import unicode_literals

import sortedm2m.fields
from django.db import migrations
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0027_auto_20160616_1650'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='command',
            name='arguments',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='pushkin.CommandArgument'),
        ),
    ]
