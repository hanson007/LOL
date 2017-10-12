#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月26日
# Company:          东方银谷
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.conf.job import *
from controller.core.public import *
from controller.core.salt_operation import Salt_Help
from controller.core.access import *
from celery import shared_task
from models import *
from cmdb.models import *
from business.models import Account
from django.shortcuts import render
from django.contrib import auth
import salt.client
import json
import os
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')


logger = logging.getLogger('job')


# Create your views here.
@login_required
def jobList(request):
    # 首页
    return render_to_response('job/JobList.html', locals(), context_instance=RequestContext(request))


@login_required
def newTaskPage(request):
    # 新建作业页面
    return render_to_response('job/newTaskPage.html', locals(), context_instance=RequestContext(request))


@login_required
@verification(CheckNewTask)
def saveNewTask(request):
    cur = Currency(request)
    dhp = Datetime_help()
    rq_post = getattr(cur, 'rq_post')
    jdata = rq_post('data')
    data = json.loads(jdata)
    nm_task = data.get('nm_task')
    nm_step = data.get('nm_step')

    nt = NmTask(nm_task, cur, dhp)
    ntObj = nt.save()

    for step in nm_step:
        ns = NmStep(step, ntObj, cur, dhp)
        ns.save()

    response = HttpResponse()
    response.write(json.dumps(u'ok'))
    return response


class NmTask(object):
    def __init__(self, nm_task, cur, dhp):
        self.name = nm_task.get('taskName')
        self.creater = cur.nowuser.username
        self.createTime = dhp.now_time

    def save(self):
        obj = Nm_Task()
        obj.name = self.name
        obj.creater = self.creater
        obj.createTime = self.createTime
        obj.save()
        logger.info(u'新建作业 %s' % self.name)
        return obj


class NmStep(object):
    def __init__(self, step, ntObj, cur, dhp):
        self.ordName = step.get('ordName', '')
        self.type = step.get('type')
        self.account = step.get('account')
        self.blockName = step.get('blockName')
        self.blockOrd = step.get('blockOrd')
        self.ord = step.get('ord')
        self.ipList = step.get('ipList')
        self.scriptTimeout = step.get('scriptTimeout')

        self.scriptId = step.get('scriptId', 0)
        self.scriptParam = step.get('scriptParam', '')

        self.fileSource = step.get('fileSource', [])
        self.fileTargetPath = step.get('fileTargetPath', '')

        self.cur = cur
        self.dhp = dhp
        self.ntObj = ntObj

    def save(self):
        obj = Nm_Step()
        obj.taskId = self.ntObj
        obj.name = self.ordName
        obj.type = self.type
        obj.ord = self.ord
        obj.blockOrd = self.blockOrd
        obj.blockName = self.blockName
        obj.account = self.account
        obj.scriptTimeout = self.scriptTimeout
        obj.creater = self.cur.nowuser.username
        obj.createTime = self.dhp.now_time

        if self.type == 1:
            script = Nm_Script.objects.get(pk=int(self.scriptId))
            self.ordName = script.name
            obj.name = self.ordName

            obj.scriptId = script
            obj.scriptParam = self.scriptParam

        if self.type == 2:
            obj.fileSource = self.fileSource
            obj.fileTargetPath = self.fileTargetPath

        obj.save()
        self.saveStepIpList(self.ipList, obj)
        logger.info(u'保存作业%s->步骤%s->节点%s' % (self.ntObj.name, self.blockName, self.ordName))

    def saveStepIpList(self, ipList, nmStep):

        for _id in ipList:
            obj = Nm_StepIplist()
            server = Server.objects.get(pk=int(_id))
            obj.ip = server.ip
            obj.step = nmStep
            obj.save()


@login_required
def getJobList(request):
    data = Nm_Task.objects.values()
    cur = Currency(request)
    nData = [cur.transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(nData))
    return response


@login_required
def editTask(request, id):
    # 编辑作业
    return render_to_response('job/editTask.html', locals(), context_instance=RequestContext(request))


@login_required
def getTask(request):
    # 获取需要编辑的作业
    cur = Currency(request)
    _id = cur.rq_post('id')
    task = Nm_Task.objects.get(pk=int(_id))
    step = Nm_Step.objects.filter(taskId=task).values()
    nStep = [cur.transfor(d) for d in step]
    nm_task = {'taskName': task.name}
    data = {'nm_task': nm_task, 'nm_step': nStep}
    import pprint
    pprint.pprint(data)
    response = HttpResponse()
    response.write(json.dumps(data))
    return response
