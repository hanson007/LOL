#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月26日
# Company:          东方银谷
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.conf.job import *
from controller.core.public import *
from controller.core.salt_operation import Salt_Help
from controller.core.access import *
from celery import shared_task
from models import *
from cmdb.models import *
from business.models import Account
from django.shortcuts import render
from django.contrib import auth
import salt.client
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Create your views here.
@login_required
def jobList(request):
    # 首页
    return render_to_response('job/JobList.html', locals(), context_instance=RequestContext(request))


@login_required
def newTaskPage(request):
    # 首页
    return render_to_response('job/newTaskPage.html', locals(), context_instance=RequestContext(request))
