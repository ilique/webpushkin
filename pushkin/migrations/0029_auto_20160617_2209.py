# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 22:09
from __future__ import unicode_literals

import sortedm2m.fields
from django.db import migrations, models
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):
    dependencies = [
        ('pushkin', '0028_auto_20160617_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='arguments',
            field=models.ManyToManyField(blank=True, to='pushkin.CommandArgument'),
        ),
        AlterSortedManyToManyField(
            model_name='commandgroup',
            name='commands',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='pushkin.Command'),
        ),
    ]
