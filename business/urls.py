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

    url(r'^account/$', account),  # 首页
    url(r'^add_account/$', add_account),  # 新增账户
    url(r'^edit_account/$', edit_account),  # 编辑账户
    url(r'^get_account/$', get_account),  # 账号信息
    url(r'^delete_account/$', delete_account),  # 删除账户

    url(r'^script/$', script),  # 脚本
    url(r'^get_script/$', get_script),  # 获取所有脚本
    url(r'^add_script_page/$', add_script_page),  # 新增脚本页面
    url(r'^save_script/$', save_script),  # 保存新增的脚本
    url(r'^edit_script_page/(?P<id>\d+)/$', edit_script_page),  # 编辑脚本页面
    url(r'^get_edit_script/$', get_edit_script),  # 获取需要编辑的脚本数据
    url(r'^edit_script/$', edit_script),  # 保存需要编辑的脚本数据

]
