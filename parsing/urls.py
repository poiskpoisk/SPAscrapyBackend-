# -*- coding: utf-8 -*-#
__author__ = 'AMA'

from django.conf.urls import url
from parsing import views

urlpatterns = [
    url(r'^stat/$',  views.statMsgList),
    url(r'^quene/$', views.queneList),
    url(r'^start/$', views.startParsing),
    url(r'^stop/$',  views.stopParsing),
    url(r'^schedule/$', views.scheduleParsing),
    url(r'^(?P<pk>[-_\d]+)/$', views.ParsingDataDetailView.as_view()),
    url(r'^list/$', views.ParsingDataListView.as_view())
]

