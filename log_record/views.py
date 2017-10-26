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
import logging
# Create your views here.
logger = logging.getLogger('log_record')


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
    nm_stepQset = Nm_StepInstance.objects.filter(pk=int(_id))
    nm_step = nm_stepQset.values().get(pk=int(_id))
    nm_step = dtf.common_transform1(nm_step)
    ipListQset = Nm_StepInstanceIpList.objects.filter(stepInstance=nm_step['id'])
    # 服务器信息
    serverInfo = []
    for ipListObj in ipListQset:
        serverQset = Server.objects.values().filter(ip=ipListObj.ip)
        if serverQset:
            serverInfo.append(dtf.common_transform1(serverQset.values()[0]))
        else:
            step = nm_stepQset[0]
            error_msg = u'作业执行历史，作业名：%s，步骤名：%s，节点名：%s，目标服务器%s不在cmdb里。' % (
                            step.taskInstanceId.name, step.blockName, step.name, ipListObj.ip)
            logger.error(error_msg)
            serverInfo.append({'ip': ipListObj.ip})
    # 执行结果
    ipList = [dtf.common_transform1(ip) for ip in ipListQset.values()]
    data = {'nm_step': nm_step, 'ipList': ipList, 'serverInfo': serverInfo}
    import pprint
    pprint.pprint(data)
    response = HttpResponse()
    response.write(json.dumps(data))
    return response
