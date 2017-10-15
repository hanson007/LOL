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
import job_management as jobMg

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # url(r'^account/$', account),  # 首页
    # url(r'^add_account/$', add_account),  # 新增账户
    # url(r'^edit_account/$', edit_account),  # 编辑账户
    # url(r'^get_account/$', get_account),  # 账号信息
    # url(r'^delete_account/$', delete_account),  # 删除账户

    url(r'^script/$', script),  # 脚本
    url(r'^run_script/$', run_script),  # 运行脚本
    url(r'^fastPushfile/$', fastPushfile),  # 快速分发文件页面
    url(r'^fastPushfile_upload_file/$', fastPushfile_upload_file),  # 上传需要快速分发的文件
    url(r'^run_fastPushfile/$', run_fastPushfile),  # 快速执行分发文件

    url(r'^jobList/$', jobMg.jobList),  # 常用作业
    url(r'^newTaskPage/$', jobMg.newTaskPage),  # 新增作业页面
    url(r'^saveNewTask/$', jobMg.saveNewTask),  # 保存新增作业
    url(r'^getJobList/$', jobMg.getJobList),  # 获取作业列表
    url(r'^editTaskPage/(?P<id>\d+)/$', jobMg.editTaskPage),  # 编辑作业页面
    url(r'^getTask/$', jobMg.getTask),  # 获取需要编辑的作业
    url(r'^editTask/$', jobMg.editTask),  # 编辑作业
    url(r'^deleteTask/$', jobMg.deleteTask),  # 删除作业
    url(r'^runTask/$', jobMg.runTask),  # 执行作业

]
