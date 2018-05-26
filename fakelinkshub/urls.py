from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home$', views.index, name='index'),
    url(r'^$', views.signIn, name='index'),
    url(r'^check_url/$', views.check_url_trustworthiness, name='url_checker'),
    url(r'^postsign/', views.postsign),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^display_urls/', views.display_links, name="display_links"),
    url(r'^signup/', views.signUp, name="signup"),
    url(r'^postsignup/', views.postsignup),
    url(r'^submit_url$', views.submit_url, name='submit'),
]
