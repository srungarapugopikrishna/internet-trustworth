# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Url, User, Repo
# Register your models here.

admin.site.register(Url)
admin.site.register(User)
admin.site.register(Repo)
