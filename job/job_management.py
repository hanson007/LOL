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
from views import (RunScriptHelp, PushFileHelp, NmInstanceHelp)
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
    response.write(json.dumps({'status': 0, 'msg': u'成功'}))
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

            obj.script = script
            obj.scriptParam = self.scriptParam

        if self.type == 2:
            obj.fileSource = json.dumps(self.fileSource)
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
    data = Nm_Task.objects.order_by('createTime').values()
    cur = Currency(request)
    nData = [cur.transfor(d) for d in data]
    response = HttpResponse()
    response.write(json.dumps(nData))
    return response


@login_required
def editTaskPage(request, id):
    # 编辑作业页面
    return render_to_response('job/editTask.html', locals(), context_instance=RequestContext(request))


@login_required
def getTask(request):
    # 获取需要编辑的作业
    cur = Currency(request)
    _id = cur.rq_post('id')
    task = Nm_Task.objects.get(pk=int(_id))
    step = Nm_Step.objects.filter(taskId=task).values()
    t = Task()
    nStep = [t.stepTransfor(d) for d in step]
    nm_task = {'taskName': task.name}
    nStep.sort(cmp=Task.cmp, reverse=True)
    data = {'nm_task': nm_task, 'nm_step': nStep}
    for d in nStep:
        print d['blockOrd'], d['ord']
    response = HttpResponse()
    response.write(json.dumps(data))
    return response


class Task(object):
    def __init__(self):
        self.dtf = DataTransfer()

    def stepTransfor(self, d):
        dict1 = self.dtf.common_transform1(d)
        ipList = self.getIpList(d['id'])
        dict1['ipList'] = ipList

        return dict1

    def getIpList(self, v):
        step = Nm_Step.objects.get(pk=int(v))
        stepIpList = Nm_StepIplist.objects.filter(step=step)
        ipList = []
        for sil in stepIpList:
            serverQset = Server.objects.filter(ip=sil.ip)
            if serverQset:
                server = serverQset.values()[0]
                server = self.dtf.common_transform1(server)
                ipList.append(server)
            else:
                error_msg = u'作业名：%s，步骤名：%s，节点名：%s，目标服务器%s不在cmdb里。' % (
                                step.taskId.name, step.blockName, step.name, sil.ip)
                logger.error(error_msg)

        return ipList

    @classmethod
    def cmp(cls, data1, data2):
        blockOrd1 = data1['blockOrd']
        blockOrd2 = data2['blockOrd']
        ord1 = data1['ord']
        ord2 = data2['ord']
        if blockOrd1 > blockOrd2:
            return -1
        elif blockOrd1 < blockOrd2:
            return 1
        elif blockOrd1 == blockOrd2:
            if ord1 > ord2:
                return -1
            elif ord1 < ord2:
                return 1
            elif ord1 == ord2:
                return 0


@login_required
@verification(CheckEditTask)
def editTask(request):
    """
    编辑作业
           先删除以前的步骤，再按照提交的步骤重新生成。
    :param request:
    :return:
    """
    cur = Currency(request)
    dhp = Datetime_help()
    rq_post = getattr(cur, 'rq_post')
    jdata = rq_post('data')
    data = json.loads(jdata)
    nm_task = data.get('nm_task')
    nm_step = data.get('nm_step')

    import pprint
    pprint.pprint(data)
    nt = EditNmTask(nm_task, cur, dhp)
    ntObj = nt.save()
    Nm_Step.objects.filter(taskId=ntObj).delete()

    for step in nm_step:
        ns = NmStep(step, ntObj, cur, dhp)
        ns.save()

    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': u'成功'}))
    return response


class EditNmTask(object):
    def __init__(self, nm_task, cur, dhp):
        self.name = nm_task.get('taskName')
        self.taskId = nm_task.get('taskId')
        self.lastModifyUser = cur.nowuser.username
        self.lastModifyTime = dhp.now_time

    def save(self):
        obj = Nm_Task.objects.get(pk=int(self.taskId))
        obj.name = self.name
        obj.lastModifyUser = self.lastModifyUser
        obj.lastModifyTime = self.lastModifyTime
        obj.save()
        logger.info(u'编辑作业 %s' % self.name)
        return obj


@login_required
def deleteTask(request):
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    for _id in data:
        Nm_Task.objects.get(pk=int(_id)).delete()
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': u'成功'}))
    return response


@login_required
def runTask(request):
    def _transfor(data):
        data['operator'] = cur.nowuser.username
        data['taskName'] = nmTask.name
        return dtf.common_transform1(data)
    cur = Currency(request)
    dtf = DataTransfer()
    taskId = cur.rq_post('taskId')
    nmTask = Nm_Task.objects.get(pk=int(taskId))
    nmStep = Nm_Step.objects.filter(taskId=nmTask).values()
    nmStep = [_transfor(data) for data in nmStep]
    nmStep.sort(cmp=Task.cmp, reverse=True)
    runNmStepAsync(nmStep, nmTask.name, cur.nowuser.username)
    # runNmStepAsync.delay(nmStep, nmTask.name, cur.nowuser.username)
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': u'成功'}))
    return response


@shared_task()
def runNmStepAsync(nmStep, taskName, operator):
    """
    执行步骤、节点
    :param nmStep:
    :return:
    """
    nmInstance = NmInstanceHelp(taskName, operator)
    nmInstance.start()
    logger.info(u'执行作业 %s, 创建作业实例' % taskName)
    error = []
    for data in nmStep:
        isStepError = False
        if data['type'] == 1:
            isStepError = runNmStepScript(data, nmInstance.instance)
        if data['type'] == 2:
            isStepError = runNmStepPushFile(data, nmInstance.instance)
        error.append(isStepError)

    isInstanceError = True if all(error) else False
    nmInstance.end()
    logger.info(u'执行作业 %s, 作业实例保存完成' % taskName)
    nmInstance.save_status(isInstanceError)
    logger.info(u'执行作业 %s, 作业实例状态保存完成，状态: %s' % (taskName, isInstanceError))


class RunNmStepScriptHelp(RunScriptHelp):
    """
    执行脚本节点
    """
    def __init__(self, data):
        super(RunNmStepScriptHelp, self).__init__(data)
        self.stepId = data.get('id')
        self.ipList = self.getIplist()
        self.target = self.saltH.getTarget(self.ipList)
        self.blockName = data.get('blockName', '')
        self.blockOrd = data.get('blockOrd', '')
        self.ord = data.get('ord', '')

    def getIplist(self):
        nmStepIpList = Nm_StepIplist.objects.filter(step=int(self.stepId))
        ipList = [nsi.ip for nsi in nmStepIpList]
        return ipList

    def stepInstance_start(self, instance):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = instance
        self.step_instance.name = self.script_name  # 节点名称=脚本名称
        self.step_instance.type = 1
        self.step_instance.ord = self.ord
        self.step_instance.blockOrd = self.blockOrd
        self.step_instance.blockName = self.blockName
        self.step_instance.account = self.account
        self.step_instance.scriptContent = self.content
        self.step_instance.scriptType = self.scriptType
        self.step_instance.scriptParam = self.scriptParam
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()


def runNmStepScript(data, instance):
    """
    运行脚本节点
    :param data: {'nm_task':nm_task, 'nm_step': nm_step}
    :return:
    """
    rssh = RunNmStepScriptHelp(data)
    logSubject = u'执行作业 %s，运行脚本节点, 步骤名：%s，节点名: %s ' % (
                    data['taskName'], rssh.blockName, rssh.script_name)
    rssh.stepInstance_start(instance)
    logger.info(logSubject + u'创建步骤实例')
    rssh.ipList_start(rssh.ipList)
    logger.info(logSubject + (u'创建作业实例目标机器。ipList: %s' % rssh.ipList))
    ret = rssh.run_job(rssh.target)
    logger.info(logSubject + (u' 执行脚本结果 %s' % ret))
    rssh.stepInstance_end()
    logger.info(logSubject + u' 步骤实例保存完成')
    is_error = rssh.save_ret(ret)
    logger.info(logSubject + u' 保存执行结果')
    rssh.save_status(is_error)
    logger.info(logSubject + (u' 保存执行状态 %s' % is_error))
    return is_error


class RunNmStepPushFileHelp(PushFileHelp):
    def __init__(self, data):
        super(RunNmStepPushFileHelp, self).__init__(data)
        self._id = data.get('id')
        self.ipList = self.getIplist()
        self.target = self.saltH.getTarget(self.ipList)
        self.fileSource = json.loads(data.get('fileSource', ''))
        self.taskName = data.get('taskName', '')
        self.blockName = data.get('blockName', '')
        self.blockOrd = data.get('blockOrd', '')
        self.ord = data.get('ord', '')
        self.name = data.get('name')  # ordName

    def stepInstance_start(self, instance):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = instance
        self.step_instance.name = self.name
        self.step_instance.type = 2
        self.step_instance.ord = self.ord
        self.step_instance.blockOrd = self.blockOrd
        self.step_instance.blockName = self.blockName
        self.step_instance.account = self.account
        self.step_instance.fileSource = json.dumps(self.fileSource)
        self.step_instance.fileTargetPath = self.fileTargetPath
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()

    def getIplist(self):
        nmStepIpList = Nm_StepIplist.objects.filter(step=int(self._id))
        ipList = [nsi.ip for nsi in nmStepIpList]
        return ipList


def runNmStepPushFile(data, instance):
    # 异步推送文件
    rsh = RunNmStepPushFileHelp(data)
    file = [f['name'] for f in rsh.fileSource]
    logSubject = u'执行作业 %s，传送文件节点 步骤名：%s，节点名: %s, 文件：%s, ' % (
                    data['taskName'], rsh.blockName, rsh.name, ' '.join(file))
    rsh.stepInstance_start(instance)
    logger.info(logSubject + u'创建步骤实例')
    rsh.ipList_start(rsh.ipList)
    logger.info(logSubject + (u'创建作业实例目标机器。ipList: %s' % rsh.ipList))
    rets = rsh.run_job(rsh.target, rsh.fileSource)
    logger.info(logSubject + (u' 执行结果 %s' % rets))
    rsh.stepInstance_end()
    logger.info(logSubject + u' 步骤实例保存完成')
    rsh.save_ret(rets)
    logger.info(logSubject + u' 保存执行结果')
    is_error = rsh.check_status(rsh.target, rsh.fileSource)
    logger.info(logSubject + u' MD5检测传输文件')
    rsh.save_status(is_error)
    logger.info(logSubject + (u' 保存执行状态 %s' % is_error))
    return is_error
