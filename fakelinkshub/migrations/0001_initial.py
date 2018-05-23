# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-06 09:44
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('url_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('url', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('frequency', models.PositiveSmallIntegerField(default=0)),
                ('pub_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user_email', models.EmailField(max_length=70, unique=True)),
                ('pub_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]