# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20170709_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='rep',
            name='rest',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
