# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.core.public import *
from controller.core.salt_operation import Salt_Help
from controller.core.access import (Check_Task, verification, Server_Help)
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
def script(request):
    # 首页
    return render_to_response('job/run_script.html', locals(), context_instance=RequestContext(request))


@login_required
@verification(Check_Task)
def run_script(request):
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    data['operator'] = cur.nowuser.username
    run_script_async.delay(data)
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response


class Run_Script_Help(object):
    def __init__(self, data):
        self.dt = Datetime_help()
        self.sh = Salt_Help()
        # self.cur = Currency(request)
        # self.jdata = self.cur.rq_post('data')
        # self.data = json.loads(self.jdata)
        self.ipList = data['ipList']
        self.scriptParam = data['scriptParam']
        self.scriptTimeout = data['scriptTimeout']
        self.account = data['account']
        self.script_name = data['script_name']
        self.scriptType = data['script_type']
        self.content = data['content']
        self.operator = data['operator']
        self.content_list = self.content.split('\n')
        self.target = ' or '.join(['S@' + ip for ip in self.ipList])

        self.instance = Nm_Instance()
        self.step_instance = Nm_StepInstance()

    def instance_start(self):
        # 作业实例 start
        self.instance.name = self.script_name
        self.instance.operator = self.operator
        self.instance.status = 2
        self.instance.startTime = self.dt.now_time
        self.instance.save()

    def stepInstance_start(self):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = self.instance
        self.step_instance.name = self.script_name
        self.step_instance.type = 1
        self.step_instance.ord = 1
        self.step_instance.blockOrd = 1
        self.step_instance.blockName = self.script_name
        self.step_instance.account = self.account
        self.step_instance.scriptContent = self.content
        self.step_instance.scriptType = 1 if self.scriptType == 'shell' else 4
        self.step_instance.scriptParam = self.scriptParam
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()

    def ipList_start(self):
        # 作业实例目标机器
        for ip in self.ipList:
            ipList = Nm_ipList()
            ipList.stepInstance_id = self.step_instance
            ipList.ip = ip
            ipList.save()

    def run_job(self):
        # 执行作业
        self.sh.delete_old_file(self.sh.file)
        self.sh.create_script_file(self.sh.file, self.content_list)
        ret = self.sh.run_script(self.target, self.sh.file, self.scriptParam, self.account, self.scriptTimeout)
        return ret

    def instance_end(self):
        # 作业实例 end
        self.instance.endTime = datetime.datetime.now()
        self.instance.totalTime = (self.instance.endTime - self.instance.startTime).seconds

    def stepInstance_end(self):
        # 作业实例步骤 end
        self.step_instance.endTime = datetime.datetime.now()
        self.step_instance.totalTime = (self.step_instance.endTime - self.step_instance.startTime).seconds

    def save_ret(self):
        # 保存结果，错误判断 is_error
        ret = self.run_job()
        server_help = Server_Help()
        servers = server_help.get_servers_dict()
        is_error = True
        for key, val in ret.items():
            ipList = Nm_ipList.objects.get(stepInstance_id=self.step_instance, ip=servers[key])
            if val['retcode'] == 0:
                result = val['stdout']
            else:
                is_error = False
                result = val['stdout'] + '\n' + val['stderr']
            ipList.result = result
            ipList.save()
        return is_error

    def save_status(self):
        # 保存执行状态(2:正在执行 3:成功 4:失败)
        is_error = self.save_ret()
        status = 3 if is_error else 4
        self.instance.status = status
        self.step_instance.status = status
        self.instance.save()
        self.step_instance.save()


@shared_task()
def run_script_async(data):
    # 异步快速运行脚本任务
    rsh = Run_Script_Help(data)
    rsh.instance_start()
    rsh.stepInstance_start()
    rsh.ipList_start()
    rsh.run_job()
    rsh.instance_end()
    rsh.stepInstance_end()
    rsh.save_ret()
    rsh.save_status()


@login_required
def fastPushfile(request):
    # 首页
    return render_to_response('job/fastPushfile.html', locals(), context_instance=RequestContext(request))


@login_required
def fastPushfile_upload_file(request):
    # 上传快速分发文件
    fileobj = request.FILES.get('file', None)
    content = fileobj.readlines()
    print fileobj.name
    # with open('/tmp/%s' % fileobj.name, 'a+') as f:
    #     f.writelines(content)
    response = HttpResponse()
    response.write(json.dumps('ok'))
    return response