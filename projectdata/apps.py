#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
from django.apps import AppConfig



class AccountAppConfig(AppConfig):
    name = "projectdata"
    verbose_name = u"生产更新获取更新数据"

    def ready(self):
        pass
