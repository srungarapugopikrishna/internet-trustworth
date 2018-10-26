# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Url, User, Repo, UrlSource
from django.contrib import auth
from urllib.parse import urlparse
from fakelinkshub.parsers.opensources_parser import parse_opensources_corpus

import pyrebase
import uuid
import json

from .dumps.snopes_dump import raw_snopes_dump

config = {
    'apiKey': "AIzaSyC12GXJRfy1J3HqBb8Lw4Pp_kaVtIpk_Z8",
    'authDomain': "trustworthyinter-1525165217599.firebaseapp.com",
    'databaseURL': "https://trustworthyinter-1525165217599.firebaseio.com",
    'projectId': "trustworthyinter-1525165217599",
    'storageBucket': "trustworthyinter-1525165217599.appspot.com",
    'messagingSenderId': "744066136741"
  }

firebase = pyrebase.initialize_app(config)

auth_firebase = firebase.auth()

database = firebase.database()


def signIn(request):
    return render(request, "signin.html")


def postsign(request):
    context = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth_firebase.sign_in_with_email_and_password(email, password)

        user_info = auth_firebase.get_account_info(user['idToken'])
        if len(user_info['users']) == 1:
            info = user_info['users'][0]
        # print('email verified:\n',info['emailVerified'])
        if info['emailVerified']:
        # print('get_account_info :: \n',auth_firebase.get_account_info(user['idToken']))
            session_id = user['idToken']
            token = get_unique_token()
            request.session['user_token'] = token
            request.session['uid'] = str(session_id)
            request.session['email'] = str(email)
            context['signedin'] = 1
        else:
            message = "A verification link is sent to your mail. Please verify your email"
            return render(request, "signin.html", {"message": message})
    # except requests.HTTPError as e:
    except Exception as e:
        exception = str(e)
        message = "Invalid credentials"
        if "INVALID_PASSWORD" in exception:
            message = "INVALID_PASSWORD"
        elif "EMAIL_NOT_FOUND" in exception:
            message = "EMAIL_NOT_FOUND"
        return render(request, "signin.html", {"message": message})
    return render(request, 'home.html', context)


def logout(request):
    try:
        request.session.pop('uid')
        request.session.pop('email')
        request.session.pop('user_token')
    except:
        pass
    auth.logout(request)
    return render(request, "signin.html")


def signUp(request):
    return render(request, "signup.html")
    # return render(request, "signUp.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirmation = request.POST.get('password_confirmation')
    if password == password_confirmation:
        try:
            user = auth_firebase.create_user_with_email_and_password(email, password)
            auth_firebase.send_email_verification(user['idToken'])
        except Exception as e:
            print('Signup exception: ',e)
            message = "Weak Password"
            exception = str(e)
            if "EMAIL_EXISTS" in exception:
                message = "EMAIL_EXISTS"
            elif "WEAK_PASSWORD" in exception:
                message = "WEAK_PASSWORD : Password should be at least 6 characters"
            return render(request, "signup.html", {"message": message})
        uid = user['localId']
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
        return render(request, "signin.html")
    else:
        message = "both passwords should be same"
        return render(request, "signup.html", {"message": message})


def index(request):
    # return render(request, 'submit_link.html')def index(request):
    return render(request, 'home.html')


def home(request):
    # return render(request, 'submit_link.html')def index(request):
    return render(request, 'home.html')


def youtube_submit_url(request):
    context = {}
    try:
        if request.session['user_token']:
            if request.method == 'POST':
                url = request.POST.get('url_field')
                email = request.session['email']
                reason = request.POST.get('other_reason')
                reason_ids = request.POST.getlist('reason_data')
                reasons = {
                    'reason_1': 'Description and video didn\'t matched',
                    'reason_2': 'Wrong thumbnail',
                    'reason_3': 'This is not a video. This is a audio file',
                    'reason_4': 'This is not the original video',
                }
                reason_output = None
                for id in reason_ids:
                    if reason_output is None:
                        reason_output = reasons[id]
                    else:
                        reason_output = reason_output + '|' + reasons[id]
                if reason:
                    reason += '|'+reason_output
                # user_obj, user_created = User.objects.get_or_create(user_email=email)
                # url_obj, url_created = Url.objects.get_or_create(url=url, reason=reason)
                # repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
                # if url_created is False:
                #     context['message'] = 'Source already reported'
                #     return render(request, 'youtube_submitter.html', context)
                # else:
                #     url_obj.save()
                #     context['message'] = 'Source reported successfully'

                return render(request, 'youtube_submitter.html', context)
            return render(request, 'youtube_submitter.html', context)
        else:
            return render(request, "signin.html")
    except KeyError or Exception as e:
        return render(request, "signin.html")


def submit_url(request):
    context = {}
    try:
        if request.session['user_token']:
            if request.method == 'POST':
                url = request.POST.get('url_field')
                email = request.session['email']
                reason = request.POST.get('url_field')
                user_obj, user_created = User.objects.get_or_create(user_email=email)
                url_obj, url_created = Url.objects.get_or_create(url=url, reason=reason)
                repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
                if url_created is False:
                    url_obj.frequency += 1
                    url_obj.save()
                return render(request, 'submit_link.html', context)
            return render(request, 'submit_link.html', context)
        else:
            return render(request, "signin.html")
    except KeyError or Exception as e:
        return render(request, "signin.html")


def display_links(request):
    context = {}
    urls = Url.objects.all()
    context['urls'] = urls
    try:
        if request.session['user_token']:
            context['signedin'] = 1
            return render(request, 'fake_links_list.html', context)
    except KeyError or Exception as e:
        return render(request, 'fake_links_list.html', context)


def check_url_trustworthiness(request):
    context = {}
    if request.method == 'POST':
        url = request.POST.get('url_field')
        try:
            url_details = Url.objects.get(url=url)
            context['url_details'] = url_details
        except:
            context['message'] = 'Source never reported'
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)


def get_unique_token():
    rand_token = uuid.uuid4().hex

    return rand_token

#
# def is_loggedin(request):
#     print('Here::::')
#     try:
#         uid = request.session['uid']
#         email = request.session['email']
#         token_id = request.session['user_token']
#         print('uid  :',uid,'  emaild  :',email,'   token_id  :',token_id)
#     except:
#         print('False::::')
#         return False
#     return True


def display_analytics(request):
    from collections import Counter
    context = {}
    urllist = []
    urls = Url.objects.all()
    for url in urls:
        parsed_url = urlparse(url.url)
        uri = '{uri.path}?{uri.query}'.format(uri=parsed_url)
        domain = parsed_url.netloc
        urllist.append(domain.replace('www.', ''))
    url_frequency = Counter(urllist)
    data = [i for i in map(lambda t: {'Name': t[0], 'Count': t[1]}, url_frequency.items())]
    print(type(data[1]), data[1])
    context['data'] = json.dumps(data)
    return render(request, 'bubble_chart.html', context)


def websites_details(request):
    context = {}
    context['data'] = parse_opensources_corpus()
    print(context)
    return render(request, 'websites_hub.html', context)


def save_source_resource(url_obj, source_url):
    url_source_obj, url_source_created = UrlSource.objects.get_or_create(url_id=url_obj)
    if url_source_created:
        url_source_obj.source_url = source_url


def scrape_dashboard(request):
    return render(request, "scrape_sites_dashboard.html")


def snopes_scrape(request):
    snopes_dump = raw_snopes_dump
    for data in snopes_dump:
        for key, value in data.items():
            print(key, '----', value)
            url = value
            email = 'admin@gmail.com'
            user_obj, user_created = User.objects.get_or_create(user_email=email)
            url_obj, url_created = Url.objects.get_or_create(url=url)
            repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
            if url_created is False:
                url_obj.frequency += 1
                url_obj.save()
            save_source_resource(url_obj, key)
    return render(request, 'scrape_sites_dashboard.html', {})

