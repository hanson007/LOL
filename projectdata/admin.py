#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
# 基础信息
from django.contrib import admin
# 本地引用
from .models import (
    EnvIronMent,
    Applications,
    Projects,
)
admin.site.register(EnvIronMent)
admin.site.register(Applications)
admin.site.register(Projects)