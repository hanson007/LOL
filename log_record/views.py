# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
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
    data = Nm_Instance.objects.all().values()
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
    instance = Nm_Instance.objects.values().get(pk=int(_id))
    nm_stepset = Nm_StepInstance.objects.filter(taskInstanceId=instance['id']).values()
    nm_step = [dtf.custom_transform1(d, **custom) for d in nm_stepset]
    nm_step.sort(cmp=Task.cmp, reverse=True)
    data = {'nm_task': dtf.custom_transform1(instance, **custom),
            'nm_step': nm_step}
    import pprint
    pprint.pprint(data)
    response = HttpResponse()
    response.write(json.dumps(data))
    return response