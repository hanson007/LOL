# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-13 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_auto_20171013_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nm_stepinstance',
            name='fileSource',
            field=models.TextField(null=True, verbose_name='\u6587\u4ef6\u4f20\u8f93\u7684\u6e90\u6587\u4ef6'),
        ),
    ]