# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_rep_rest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event',
            field=models.CharField(choices=[('50 free', '50 Freestyle'), ('100 free', '100 Freestyle'), ('200 free', '200 Freestyle'), ('500 free', '500 Freestyle'), ('1000 free', '1000 Freestyle'), ('50 back', '50 Backstroke'), ('100 back', '100 Backstroke'), ('200 back', '200 Backstroke'), ('50 breast', '50 Breaststroke'), ('100 breast', '100 Breaststroke'), ('200 breast', '200 Breaststroke'), ('50 fly', '50 Butterfly'), ('100 fly', '100 Butterfly'), ('200 fly', '200 Butterfly')], max_length=10),
        ),
    ]
