# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.core.validators import URLValidator
import uuid


class Url(models.Model):
    url_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    url = models.TextField(validators=[URLValidator()])
    url_title = models.TextField()
    reason = models.TextField(default=None)
    frequency = models.PositiveSmallIntegerField(default=1)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user_email = models.EmailField(max_length=70, null=False, blank=False, unique=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


class Repo(models.Model):
    repo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    url_id = models.ForeignKey(Url, default=None, blank=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, default=None, blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


# class token(models.Model):
#     token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
#     user_id = models.ForeignKey(User, default=None, blank=True)
#     timestamp = models.DateTimeField(default=datetime.now, blank=True)


class UrlSource(models.Model):
    resource_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    url_id = models.ForeignKey(Url, default=None, blank=True, on_delete=models.CASCADE)
    source_url = models.TextField(validators=[URLValidator()])
    timestamp = models.DateTimeField(default=datetime.now, blank=True)


# class DomainHub(models.Model):
#     domain_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
#     domain_name = models.TextField(validators=[URLValidator()])
#     domain_title = models.TextField()
#     domain_type = models.TextField()