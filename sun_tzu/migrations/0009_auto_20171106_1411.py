# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-06 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sun_tzu', '0008_player_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='card_number',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='player',
            name='played_one',
            field=models.BooleanField(default=False),
        ),
    ]
