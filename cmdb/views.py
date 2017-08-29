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
def index(request):
    # 首页
    return render_to_response('cmdb/index.html', locals(), context_instance=RequestContext(request))


@login_required
def add_server(request):
    # 添加机器
    cur = Currency(request)
    ip = cur.rq_post('ip')
    desc = cur.rq_post('desc')
    obj = Server()
    obj.ip = ip
    obj.desc = desc
    obj.creater = cur.nowuser
    obj.ModifyUser = cur.nowuser
    obj.save()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def get_index(request):
    # 获取服务器列表
    data = Server.objects.all().values()
    cur = Currency(request)
    data_str = [cur.transfor(d) for d in data]
    print data_str
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response