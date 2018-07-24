# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 06:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20180724_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 6, 1, 54, 248737, tzinfo=utc), help_text='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 6, 1, 54, 248775, tzinfo=utc), help_text='最后修改时间'),
        ),
    ]