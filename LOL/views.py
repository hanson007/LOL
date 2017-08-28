# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
import json

# Create your views here.
@login_required
def index(request):
    # 首页
    nowuser = auth.get_user(request)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


@login_required
def get_username(request):
    # 获取当前登陆的用户名
    nowuser = auth.get_user(request)
    username = nowuser.get_username()
    response = HttpResponse()
    response.write(json.dumps(username))
    return response