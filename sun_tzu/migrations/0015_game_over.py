# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-07 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sun_tzu', '0014_auto_20171107_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='over',
            field=models.BooleanField(default=False),
        ),
    ]