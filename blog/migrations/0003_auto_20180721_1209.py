# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-21 04:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180721_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 21, 4, 9, 5, 798432, tzinfo=utc), help_text='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 21, 4, 9, 5, 798491, tzinfo=utc), help_text='最后修改时间'),
        ),
    ]
