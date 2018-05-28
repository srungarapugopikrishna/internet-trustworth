# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Url, User, Repo
from django.contrib import auth
import pyrebase
import uuid

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
    return render(request, "signIn.html")


def postsign(request):
    context = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth_firebase.sign_in_with_email_and_password(email, password)
        session_id = user['idToken']
        token = get_unique_token()
        request.session['user_token'] = token
        request.session['uid'] = str(session_id)
        request.session['email'] = str(email)
        context['signedin'] = 1
    except Exception as e:
        print('error : ', e)
        message = "Invalid credentials"
        return render(request, "signIn.html", {"message": message})
    return render(request, 'home.html', context)


def logout(request):
    try:
        request.session.pop('uid')
        request.session.pop('email')
        request.session.pop('user_token')
    except:
        pass
    auth.logout(request)
    return render(request, "signIn.html")


def signUp(request):

    return render(request, "signUp.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth_firebase.create_user_with_email_and_password(email, password)
    except:
        message = "Weak Password"
        return render(request, "signUp.html", {"message": message})
    uid = user['localId']
    data = {"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request, "signIn.html")


def index(request):
    # return render(request, 'submit_link.html')def index(request):
    return render(request, 'home.html')


def home(request):
    # return render(request, 'submit_link.html')def index(request):
    return render(request, 'home.html')


def submit_url(request):
    context = {}
    try:
        if request.session['user_token']:
            if request.method == 'POST':
                url = request.POST.get('url_field')
                email = request.session['email']
                user_obj, user_created = User.objects.get_or_create(user_email=email)
                url_obj, url_created = Url.objects.get_or_create(url=url)
                repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
                if url_created is False:
                    url_obj.frequency += 1
                    url_obj.save()
                return render(request, 'submit_link.html', context)
            return render(request, 'submit_link.html', context)
        else:
            return render(request, "signIn.html")
    except KeyError or Exception as e:
        return render(request, "signIn.html")


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

