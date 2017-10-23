# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.core.public import *
from controller.core.access import *
from models import *
from django.shortcuts import render
from django.contrib import auth
import json


# Create your views here.
@login_required
def account(request):
    # 首页
    return render_to_response('business/account.html', locals(), context_instance=RequestContext(request))


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
    # 脚本首页
    return render_to_response('business/script.html', locals(), context_instance=RequestContext(request))


# Create your views here.
@login_required
def get_script(request):
    # 获取所有脚本
    data = Nm_Script.objects.all().values()
    cur = Currency(request)
    data_str = [cur.transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response


@login_required
def add_script_page(request):
    # 新增脚本首页
    return render_to_response('business/add_script.html', locals(), context_instance=RequestContext(request))


@login_required
@verification(Check_AddScript)
def save_script(request):
    # 保存新增的脚本
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    obj = Nm_Script()
    obj.name = data['script_name']
    obj.content = data['content']
    obj.TYPE = data['script_type']
    obj.creater = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response


@login_required
def edit_script_page(request, id):
    # 编辑脚本页面
    return render_to_response('business/edit_script.html', locals(), context_instance=RequestContext(request))


@login_required
def get_edit_script(request):
    # 获取需要编辑的脚本数据
    cur = Currency(request)
    _id = cur.rq_post('id')
    script = Nm_Script.objects.get(pk=int(_id))
    data = {'name': script.name, 'content': script.content, 'TYPE': script.TYPE}
    response = HttpResponse()
    response.write(json.dumps(data))
    return response


@login_required
@verification(Check_EditScript)
def edit_script(request):
    # 保存需要编辑的脚本数据
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    obj = Nm_Script.objects.get(pk=int(data['script_id']))
    obj.name = data['script_name']
    obj.content = data['content']
    obj.TYPE = data['script_type']
    obj.ModifyUser = cur.nowuser.username
    obj.save()
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response