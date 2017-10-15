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
from views import (run_script_async, Run_Script_Help)
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
        dict1 = self.dtf.commonTransfor1(d)
        ipList = self.getIpList(d['id'])
        dict1['ipList'] = ipList

        return dict1

    def getIpList(self, v):
        step = Nm_Step.objects.get(pk=int(v))
        stepIpList = Nm_StepIplist.objects.filter(step=step)
        ipList = []
        for sil in stepIpList:
            server = Server.objects.filter(ip=sil.ip).values()[0]
            server = self.dtf.commonTransfor1(server)
            ipList.append(server)

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
    cur = Currency(request)
    taskId = cur.rq_post('taskId')
    nmTask = Nm_Task.objects.get(pk=int(taskId))
    nmStep = Nm_Step.objects.filter(taskId=nmTask).values()
    for data in nmStep:
        data['operator'] = cur.nowuser.username
        data['taskName'] = nmTask.name
    nmStep = list(nmStep)
    nmStep.sort(cmp=Task.cmp, reverse=True)
    for d in nmStep:
        print d['blockOrd'], d['ord']
    runNmStepAsync(nmStep)
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': u'成功'}))
    return response


@shared_task()
def runNmStepAsync(nmStep):
    """
    执行步骤、节点
    :param nmStep:
    :return:
    """
    import pprint

    for data in nmStep:
        # print pprint.pprint(data)
        if data['type'] == 1:
            runNmStepScript(data)
        if data['type'] == 2:
            runNmStepPushFile(data)


class RunNmStepScriptHelp(Run_Script_Help):
    """
    执行脚本节点
    """
    def __init__(self, data):
        self._id = data.get('id')
        self.ipList = self.getIplist()
        self.dt = Datetime_help()
        self.sh = Salt_Help()
        self.scriptParam = data.get('scriptParam', '')
        self.scriptTimeout = data.get('scriptTimeout', '')
        self.account = data.get('account', '')
        self.script_id = data.get('script_id', '')
        self.operator = data.get('operator', '')
        self.blockName = data.get('blockName', '')
        self.blockOrd = data.get('blockOrd', '')
        self.ord = data.get('ord', '')
        self.target = ' or '.join(['S@' + ip for ip in self.ipList])

        self.instance = Nm_Instance()
        self.step_instance = Nm_StepInstance()

        if self.script_id:
            script = Nm_Script.objects.get(pk=int(self.script_id))
            self.script_name = script.name
            self.content = script.content
            self.scriptType = script.TYPE

        self.content_list = self.content.split('\n')

    def getIplist(self):
        nmStepIpList = Nm_StepIplist.objects.filter(step=int(self._id))
        ipList = [nsi.ip for nsi in nmStepIpList]
        return ipList

    def stepInstance_start(self):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = self.instance
        self.step_instance.name = self.script_name
        self.step_instance.type = 1
        self.step_instance.ord = self.ord
        self.step_instance.blockOrd = self.blockOrd
        self.step_instance.blockName = self.blockName
        self.step_instance.account = self.account
        self.step_instance.scriptContent = self.content
        self.step_instance.scriptType = 1 if self.scriptType == 'shell' else 4
        self.step_instance.scriptParam = self.scriptParam
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()


def runNmStepScript(data):
    rssh = RunNmStepScriptHelp(data)
    rssh.instance_start(data['taskName'])
    rssh.stepInstance_start()
    rssh.ipList_start()
    ret = rssh.run_job()
    rssh.instance_end()
    rssh.stepInstance_end()
    is_error = rssh.save_ret(ret)
    rssh.save_status(is_error)


class RunNmStepPushFileHelp(Run_Script_Help):
    def __init__(self, data):
        self._id = data.get('id')
        self.ipList = self.getIplist()
        self.dt = Datetime_help()
        self.sh = Salt_Help()
        self.scriptTimeout = data.get('scriptTimeout', '')
        self.account = data.get('account', '')
        self.operator = data.get('operator', '')
        self.blockName = data.get('blockName', '')
        self.blockOrd = data.get('blockOrd', '')
        self.ord = data.get('ord', '')
        self.target = ' or '.join(['S@' + ip for ip in self.ipList])

        self.instance = Nm_Instance()
        self.step_instance = Nm_StepInstance()

        self.name = data.get('name')  # ordName
        self.taskName = data.get('taskName')
        self.fileSource = json.loads(data.get('fileSource'))
        self.fileTargetPath = data.get('fileTargetPath')
        # 目标路径最后一位如果没有反斜线 /，那么就加一个
        if not self.fileTargetPath.rfind('/') == (len(self.fileTargetPath) - 1):
            self.fileTargetPath += '/'

    def stepInstance_start(self):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = self.instance
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

    def run_job(self):
        # 执行作业
        rets = {}
        for file in self.fileSource:
            ret = self.sh.run_fastPushfile(self.target,
                                           file['name'],
                                           self.fileTargetPath,
                                           self.account, self.scriptTimeout)
            print 'job===>',ret
            self.merge_results(rets, ret)
        return rets

    def merge_results(self, rets, ret):
        """
        将每台机器多个文件的传输结果合并为一个。
        例如file1、file2 传输到master机器上返回两个结果{'master': v1}, {'master': v2}
        将这两个结果合并为一个，保证每台机器只有一个结果
        :param rets: {'master': m_v1+ m_v2, 'test': t_v1+t_v2, ... ...}
        :param ret: [ {'master': m_v1, 'test': t_v1} ,{'master': m_v2, 'test': t_v2}, ... ... ]
        :return:
        """
        for k, v in ret.items():
            if k in rets:
                rets[k] = rets[k] + '\n' + v
            else:
                rets[k] = v

    def save_ret(self, ret):
        # 保存结果，错误判断 is_error
        server_help = Server_Help()
        servers = server_help.get_servers_dict()
        for key, val in ret.items():
            ipList = Nm_StepInstanceIpList.objects.get(stepInstance_id=self.step_instance, ip=servers[key])
            ipList.result = val
            ipList.save()

    def check_status(self):
        # 利用md5检测传输文件是否成功，有一个失败，那么任务就算失败
        rets = []
        for file in self.fileSource:
            # 获取文件的md5值
            md5 = self.sh.get_file_md5(file['name'])
            # 检测传输的文件md5值
            ret = self.sh.check_file_md5(self.target,
                                        file['name'],
                                        self.fileTargetPath, md5)
            rets.extend(ret.values())

        return True if all(rets) else False


def runNmStepPushFile(data):
    # 异步推送文件
    rsh = RunNmStepPushFileHelp(data)
    rsh.instance_start(rsh.taskName)
    rsh.stepInstance_start()
    rsh.ipList_start()
    rets = rsh.run_job()
    rsh.instance_end()
    rsh.stepInstance_end()
    rsh.save_ret(rets)
    is_error = rsh.check_status()
    rsh.save_status(is_error)