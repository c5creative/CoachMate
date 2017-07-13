# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 01:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_auto_20170711_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='user',
        ),
        migrations.RemoveField(
            model_name='week',
            name='start',
        ),
        migrations.RemoveField(
            model_name='week',
            name='team',
        ),
        migrations.AddField(
            model_name='practice',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Team'),
        ),
        migrations.AddField(
            model_name='week',
            name='current',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='week',
            name='friday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='monday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='saturday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='sunday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='thursday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='tuesday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='week',
            name='wednesday',
            field=models.DateField(null=True),
        ),
    ]
