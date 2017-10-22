# -*- coding: UTF-8 -*-
"""LOL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^taskInstanceList/$', taskInstanceList),  # 作业实例列表
    url(r'^get_taskInstance_list/$', get_taskInstance_list),  # 获取所有作业实例数据
    url(r'^task_instance/(?P<id>\d+)/$', task_instance),  # 作业详情
    url(r'^get_task_instance/$', get_task_instance),  # 获取作业实例数据
    url(r'^taskStepInstance/(?P<id>\d+)/$', taskStepInstance),  # 作业实例步骤
    url(r'^loadTaskStepInstance/$', loadTaskStepInstance),  # 加载作业实例步骤数据

    # url(r'^script/$', script),  # 脚本

]
