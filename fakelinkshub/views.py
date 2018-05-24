# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Url, User, Repo
from django.contrib import auth
import pyrebase


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
    return render(request,"signIn.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth_firebase.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid credentials"
        return render(request, "signIn.html", {"message": message})
    # print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    request.session['email'] = str(email)
    # return render(request,"welcome.html", {"mail":email})
    return render(request, 'submit_link.html')


def logout(request):
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
    return render(request, 'submit_link.html')


def submit_url(request):
    context = {}
    if request.method == 'POST':
        url = request.POST.get('url_field')
        # email = request.POST.get('email_field')
        email = request.session['email']
        user_obj, user_created = User.objects.get_or_create(user_email=email)
        url_obj, url_created = Url.objects.get_or_create(url=url)
        repo_obj, repo_created = Repo.objects.get_or_create(url_id=url_obj, user_id=user_obj)
        if url_created is False:
            url_obj.frequency += 1
            url_obj.save()
        return render(request, 'submit_link.html', context)
    return render(request, 'submit_link.html', context)

