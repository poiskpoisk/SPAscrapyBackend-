# -*- coding: utf-8 -*-#
__author__ = 'AMA'

from rest_framework import serializers
from .models import StatMsg, QueneURLs


class StatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatMsg
        fields = ('id', 'parsingURL', 'msg')


class QueneMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueneURLs
        fields = ('parsingURL', )