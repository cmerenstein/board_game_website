# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-03 06:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sun_tzu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_position', models.IntegerField()),
                ('is_single_use', models.BooleanField()),
                ('card_value', models.CharField(max_length=3)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sun_tzu.Player')),
            ],
        ),
    ]
