# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-06 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakelinkshub', '0002_repo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Urls',
            new_name='Url',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]