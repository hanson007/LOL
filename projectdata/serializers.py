#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function

__author__ = 'xuebk'
from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)