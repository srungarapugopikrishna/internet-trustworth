# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.core.validators import URLValidator
import uuid


class Url(models.Model):
    url_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    url = models.TextField(validators=[URLValidator()])
    frequency = models.PositiveSmallIntegerField(default=1)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user_email = models.EmailField(max_length=70, null=False, blank=False, unique=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


class Repo(models.Model):
    repo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    url_id = models.ForeignKey(Url, default=None, blank=True)
    user_id = models.ForeignKey(User, default=None, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
