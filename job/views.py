# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.core.public import *
from controller.core.salt_operation import Salt_Help
from controller.core.access import (Check_Task, verification)
from models import *
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
def script(request):
    # 首页
    return render_to_response('job/run_script.html', locals(), context_instance=RequestContext(request))


@login_required
@verification(Check_Task)
def run_script(request):
    dt = Datetime_help()
    sh = Salt_Help(request)
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    ipList = data['ipList']
    scriptParam = data['scriptParam']
    scriptTimeout = data['scriptTimeout']
    account = data['account']
    script_name = data['script_name']
    content = data['content']
    content_list = content.split('\n')
    target = ' or '.join(['S@' + ip for ip in ipList])

    sh.delete_old_file(sh.file)
    sh.write_file(sh.file, content_list)
    ret = sh.run_script(target, sh.file, scriptParam, account, scriptTimeout)

    # instance = Nm_Instance()
    # instance.name = script_name
    # instance.operator = cur.nowuser.username
    # instance.status = 3
    # instance.startTime = dt.now_time
    # instance.endTime = dt.now_time
    # instance.totalTime = 3
    # instance.save()
    #
    # step_instance = Nm_StepInstance
    # step_instance.taskInstanceId = instance
    # step_instance.name = script_name
    # step_instance.type = 1
    # step_instance.ord = 1
    # step_instance.blockOrd = 1
    # step_instance.blockName = script_name
    # step_instance.account = account
    # step_instance.scriptContent = content
    # step_instance.scriptType = 1
    # step_instance.scriptParam = scriptParam
    # step_instance.scriptTimeout = scriptTimeout
    # step_instance.operator = cur.nowuser.username
    # step_instance.status = 3
    # step_instance.startTime = dt.now_time
    # step_instance.endTime = dt.now_time
    # step_instance.totalTime = 3
    # step_instance.save()
    #
    # ipList = Nm_ipList()
    # ipList.stepInstance_id = step_instance
    # ipList.ip = u'192.168.93.135'
    # ipList.result = u'1234....'
    # ipList.save()


    print ret
    for k, v in ret.items():
        print k, v
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response
