# -*- coding: utf-8 -*-#
__author__ = 'AMA'

from django.conf.urls import url
from parsing import views

urlpatterns = [
    url(r'^stat/$',  views.statMsgList),
    url(r'^quene/$', views.queneList),
]

