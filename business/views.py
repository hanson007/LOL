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
    return render_to_response('business/../templates/log_record/account.html', locals(), context_instance=RequestContext(request))


@login_required
def add_account(request):
    # 添加账户
    cur = Currency(request)
    name = cur.rq_post('name')
    desc = cur.rq_post('desc')
    obj = Account()
    obj.name = name
    obj.desc = desc
    obj.creater = cur.nowuser.username
    obj.ModifyUser = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def get_account(request):
    # 获取账号列表
    data = Account.objects.all().values()
    cur = Currency(request)
    data_str = [cur.transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response


@login_required
def edit_account(request):
    # 编辑机器
    cur = Currency(request)
    name = cur.rq_post('name')
    desc = cur.rq_post('desc')
    _id = cur.rq_post('id')
    obj = Account.objects.get(pk=int(_id))
    obj.name = name
    obj.desc = desc
    obj.ModifyUser = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


@login_required
def delete_account(request):
    # 删除账号
    cur = Currency(request)
    data = cur.rq_post('data')
    data = json.loads(data)
    for _id in data:
        Account.objects.get(pk=int(_id)).delete()
    response = HttpResponse()
    response.write(json.dumps('成功'))
    return response


# Create your views here.
@login_required
def script(request):
    # 首页
    return render_to_response('business/script.html', locals(), context_instance=RequestContext(request))
