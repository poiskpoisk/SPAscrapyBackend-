# -*- coding: utf-8 -*-#
__author__ = 'AMA'

from rest_framework import serializers
from .models import StatMsg, QueneURLs, ScheduleQuene


class StatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatMsg
        fields = ('parsingURL', 'msg',)


class QueneMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueneURLs
        fields = ('parsingURL',)


class ScheduleQueneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleQuene
        fields = ('strDataTime',)