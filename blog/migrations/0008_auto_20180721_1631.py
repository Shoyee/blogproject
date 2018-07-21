# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-21 08:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180721_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 21, 8, 31, 15, 616065, tzinfo=utc), help_text='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 21, 8, 31, 15, 616103, tzinfo=utc), help_text='最后修改时间'),
        ),
    ]
