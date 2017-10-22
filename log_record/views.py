# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from cmdb.models import Server
from job.models import *
from job.job_management import (Task)
from controller.core.public import *
from controller.conf.job import STATUS_TABLE
import json
# Create your views here.


@login_required
def taskInstanceList(request):
    # 作业实例列表首页
    return render_to_response('log_record/taskInstanceList.html', locals(), context_instance=RequestContext(request))


@login_required
def get_taskInstance_list(request):
    # 获取所有作业实例
    data = Nm_Instance.objects.all().order_by('-createTime').values()
    data_str = [transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response


def transfor(d):
    status_list = {3: u'执行成功', 4: u'执行失败', 2: u'正在执行'}
    dict1 = {}
    for k, v in d.items():
        if isinstance(v, datetime.datetime):
            v = v.strftime("%Y-%m-%d %H:%M:%S")
        dict1[k] = v
        if k == 'status':
            dict1[k] = status_list[v]

    return dict1


@login_required
def task_instance(request, id):
    # 作业详情
    return render_to_response('log_record/taskInstance.html', locals(), context_instance=RequestContext(request))


@login_required
def get_task_instance(request):
    # 获取作业实例
    cur = Currency(request)
    _id = cur.rq_post('taskInstanceId')
    dtf = DataTransfer()
    custom = {'status': STATUS_TABLE}

    def _transfor(step):
        step = dtf.custom_transform1(step, **custom)
        ipCount = Nm_StepInstanceIpList.objects.filter(stepInstance=step['id']).count()
        step['ipCount'] = ipCount
        return step

    instance = Nm_Instance.objects.values().get(pk=int(_id))
    nm_step = Nm_StepInstance.objects.filter(taskInstanceId=instance['id']).values()
    nm_step = [_transfor(d) for d in nm_step]
    nm_step.sort(cmp=Task.cmp, reverse=True)
    data = {'nm_task': dtf.custom_transform1(instance, **custom),
            'nm_step': nm_step}
    import pprint
    pprint.pprint(data)
    response = HttpResponse()
    response.write(json.dumps(data))
    return response


@login_required
def taskStepInstance(request, id):
    # 作业详情
    return render_to_response('log_record/taskStepInstance.html', locals(), context_instance=RequestContext(request))


@login_required
def loadTaskStepInstance(request):
    # 获取作业步骤实例数据
    cur = Currency(request)
    _id = cur.rq_post('stepId')
    dtf = DataTransfer()
    nm_step = Nm_StepInstance.objects.values().get(pk=int(_id))
    nm_step = dtf.common_transform1(nm_step)
    ipListQset = Nm_StepInstanceIpList.objects.filter(stepInstance=nm_step['id'])
    # 服务器信息
    serverInfo = [dtf.common_transform1(Server.objects.values().get(ip=ip)) for ip in ipListQset]
    # 执行结果
    ipList = [dtf.common_transform1(ip) for ip in ipListQset.values()]
    data = {'nm_step': nm_step, 'ipList': ipList, 'serverInfo': serverInfo}
    import pprint
    pprint.pprint(data)
    response = HttpResponse()
    response.write(json.dumps(data))
    return response
