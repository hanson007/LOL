#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# 调用 projectdata 接口
import viewsets as projectdata
urlpatterns = format_suffix_patterns([
    url(
        r'^projectdata/get_data/$',
        projectdata.GetData.as_view(),
        name='projectdata-get_hosts',
    ),
    url(
        r'^projectdata/get_shell/$',
        projectdata.get_shell.as_view(),
        name='projectdata-get_hosts',
    ),
])
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####