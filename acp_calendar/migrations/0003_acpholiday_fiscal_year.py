# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-27 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acp_calendar', '0002_load_holiday_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='acpholiday',
            name='fiscal_year',
            field=models.IntegerField(default=0, verbose_name='fiscal year'),
        ),
    ]
