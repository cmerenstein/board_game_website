# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-02 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sun_tzu', '0004_auto_20171102_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='id',
        ),
        migrations.AlterField(
            model_name='game',
            name='game_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]