# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-06 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sun_tzu', '0006_auto_20171104_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='played_one',
            field=models.BooleanField(default=True),
        ),
    ]
