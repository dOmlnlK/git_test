"""myFortress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^web_ssh', views.web_ssh, name="web_ssh"),
    url(r'^login/$', views.acc_login),
    url(r'^logout/$', views.acc_logout),
    url(r'^logout/$', views.acc_logout),
    url(r'^host_mgr/batch_cmd/$', views.batch_cmd,name='batch_cmd'),
    url(r'^host_mgr/file_transfer/$', views.file_transfer,name='file_transfer'),
    url(r'^batch_task_mgr/$', views.batch_task_mgr, name='batch_task_mgr'),
    url(r'^get_task_result/$', views.task_result, name='get_task_result'),
]
