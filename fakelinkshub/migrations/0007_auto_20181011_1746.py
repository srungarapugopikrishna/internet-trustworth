# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fakelinkshub', '0006_auto_20181011_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='reason',
            field=models.TextField(default=None),
        ),
    ]
