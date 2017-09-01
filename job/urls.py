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

    # url(r'^account/$', account),  # 首页
    # url(r'^add_account/$', add_account),  # 新增账户
    # url(r'^edit_account/$', edit_account),  # 编辑账户
    url(r'^get_account/$', get_account),  # 账号信息
    # url(r'^delete_account/$', delete_account),  # 删除账户

    url(r'^run_script/$', run_script),  # 脚本

]
