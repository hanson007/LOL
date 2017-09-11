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
    hostname = cur.rq_post('hostname')
    desc = cur.rq_post('desc')
    obj = Server()
    obj.ip = ip
    obj.hostname = hostname
    obj.desc = desc
    obj.creater = cur.nowuser.username
    obj.ModifyUser = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def edit_server(request):
    # 编辑机器
    cur = Currency(request)
    ip = cur.rq_post('ip')
    hostname = cur.rq_post('hostname')
    desc = cur.rq_post('desc')
    _id = cur.rq_post('id')
    obj = Server.objects.get(pk=int(_id))
    obj.ip = ip
    obj.hostname = hostname
    obj.desc = desc
    obj.ModifyUser = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def delete_server(request):
    # 删除机器
    cur = Currency(request)
    data = cur.rq_post('data')
    data = json.loads(data)
    for _id in data:
        Server.objects.get(pk=int(_id)).delete()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def get_index(request):
    # 获取服务器列表
    data = Server.objects.all().values()
    cur = Currency(request)
    data_str = [cur.transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response