# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Url, User, Repo

import pprint


def index(request):
    return render(request, 'submit_link.html')


def submit_url(request):
    context = {}
    if request.method == 'POST':
        url = request.POST.get('url_field')
        email = request.POST.get('email_field')
        user_obj, user_created = User.objects.get_or_create(user_email=email)
        url_obj, url_created = Url.objects.get_or_create(url=url)
        repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
        if url_created is False:
            url_obj.frequency += 1
            url_obj.save()
        return render(request, 'submit_link.html', context)
    return render(request, 'submit_link.html', context)

