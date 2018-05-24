from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.signIn, name='index'),
    url(r'^postsign/', views.postsign),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^signup/', views.signUp, name="signup"),
    url(r'^postsignup/', views.postsignup),
    url(r'^submit_url$', views.submit_url, name='submit'),
]
