# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.core.public import *
from models import *
from django.shortcuts import render
from django.contrib import auth
import json


# Create your views here.
@login_required
def account(request):
    # 首页
    return render_to_response('business/account.html', locals(), context_instance=RequestContext(request))
