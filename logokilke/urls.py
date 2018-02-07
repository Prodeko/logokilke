from django.conf.urls import url
from django.contrib.auth import views as auth_views

from logokilke.views import *
from logokilke.views_api import *
from logokilke import views

urlpatterns = [

    # Auth
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Client
    url(r'^$', views.index, name='index'),
    url(r'^single/$', views.single, name='single'),
    url(r'^single/upload/$', views.upload_pic, name='upload_pic'),
    url(r'^multi/$', views.multi, name='multi'),


    # API
    url(r'^api-request/$', APIRequestView.as_view(), name='api_request'),
]
