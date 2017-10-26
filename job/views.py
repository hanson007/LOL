# -*- coding: UTF-8 -*-
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
import logging
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger('job')


# Create your views here.
@login_required
def script(request):
    # 首页
    return render_to_response('job/run_script.html', locals(), context_instance=RequestContext(request))


@login_required
@verification(Check_Task)
def run_script(request):
    """
    快速执行脚本
    :param request:
    :return:
    """
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    data['operator'] = cur.nowuser.username
    # run_script_async.delay(data)
    run_script_async(data)
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response


class NmInstanceHelp(object):
    def __init__(self, taskName, operator):
        self.dt = Datetime_help()
        self.instance = Nm_Instance()
        self.taskName = taskName
        self.operator = operator

    def start(self):
        # 作业实例 start
        self.instance.name = self.taskName
        self.instance.operator = self.operator
        self.instance.status = 2
        self.instance.startTime = self.dt.now_time
        self.instance.save()

    def end(self):
        # 作业实例 end
        self.instance.endTime = datetime.datetime.now()
        timeDifference = (self.instance.endTime - self.instance.startTime).total_seconds()
        self.instance.totalTime = round(timeDifference, 3)

    def save_status(self, is_error):
        # 保存执行状态(2:正在执行 3:成功 4:失败)
        status = 3 if is_error else 4
        self.instance.status = status
        self.instance.save()


class RunTaskHelp(object):
    """
    作业运行帮助
    """
    def __init__(self, data):
        self.dt = Datetime_help()
        self.saltH = Salt_Help()
        self.scriptTimeout = data.get('scriptTimeout', '')
        self.account = data.get('account', '')
        self.operator = data.get('operator', '')

        self.step_instance = Nm_StepInstance()

    def stepInstance_end(self):
        # 作业实例步骤 end
        self.step_instance.endTime = datetime.datetime.now()
        timeDifference = (self.step_instance.endTime - self.step_instance.startTime).total_seconds()
        self.step_instance.totalTime = round(timeDifference, 3)

    def ipList_start(self, ipList):
        # 作业实例目标机器
        for ip in ipList:
            ipList = Nm_StepInstanceIpList()
            ipList.stepInstance = self.step_instance
            ipList.ip = ip
            ipList.save()

    def save_status(self, is_error):
        # 保存执行状态(2:正在执行 3:成功 4:失败)
        status = 3 if is_error else 4
        self.step_instance.status = status
        self.step_instance.save()


class RunScriptHelp(RunTaskHelp):
    """
    运行脚本帮助
    """
    def __init__(self, data):
        super(RunScriptHelp, self).__init__(data)
        self.scriptParam = data.get('scriptParam', '')
        self.script_id = data.get('script_id', '')

        script = Nm_Script.objects.get(pk=int(self.script_id))
        self.script_name = script.name
        self.content = script.content
        self.scriptType = script.TYPE

        self.content_list = self.content.split('\n')

    def ipList(self, val):
        return val

    def run_job(self, target):
        # 执行作业
        self.saltH.delete_old_file(self.saltH.file)
        self.saltH.create_script_file(self.saltH.file, self.content_list)
        ret = self.saltH.run_script(target, self.saltH.file, self.scriptParam, self.account, self.scriptTimeout)
        return ret

    def save_ret(self, ret):
        # 保存结果，错误判断 is_error(True：执行报错，False：执行成功)
        server_help = Server_Help()
        servers = server_help.get_servers_dict1()
        is_error = True
        for key, val in ret.items():
            if key not in servers:
                logger.error(u'主机名错误 %s %s' % (key, servers))
                is_error = False
                continue
            ipList = Nm_StepInstanceIpList.objects.get(stepInstance=self.step_instance, ip=servers[key])
            try:
                if val['retcode'] == 0:
                    result = val['stdout']
                else:
                    is_error = False
                    result = val['stdout'] + '\n' + val['stderr']
            except TypeError:
                is_error = False
                errorMsg = u'%s 执行 %s 脚本失败，返回结果类型错误' % (key, self.script_name)
                result = val
                logger.error(errorMsg)
            except Exception as e:
                is_error = False
                errorMsg = u'%s 执行 %s 脚本失败，返回结果未知错误类型 %s' % (key, self.script_name, e)
                result = val
                logger.error(errorMsg)
            ipList.result = result
            ipList.save()
        return is_error


class FastRunScriptHelp(RunScriptHelp):
    """
    快速执行脚本
    """
    def __init__(self, data):
        super(FastRunScriptHelp, self).__init__(data)
        self.ipList = data.get('ipList', '')
        self.target = self.saltH.getTarget(self.ipList)

    def stepInstance_start(self, instance):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = instance
        self.step_instance.name = self.script_name
        self.step_instance.type = 1
        self.step_instance.ord = 1
        self.step_instance.blockOrd = 1
        self.step_instance.blockName = self.script_name
        self.step_instance.account = self.account
        self.step_instance.scriptContent = self.content
        self.step_instance.scriptType = self.scriptType
        self.step_instance.scriptParam = self.scriptParam
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()


@shared_task()
def run_script_async(data):
    # 异步快速运行脚本任务

    rsh = FastRunScriptHelp(data)
    script_id = data['script_id']
    nmScript = Nm_Script.objects.get(pk=int(script_id))
    nmInstance = NmInstanceHelp(nmScript.name, data['operator'])
    nmInstance.start()
    logger.info(u'快速执行脚本 %s, 创建作业实例' % nmScript.name)
    rsh.stepInstance_start(nmInstance.instance)
    logger.info(u'快速执行脚本 %s, 创建作业步骤实例' % nmScript.name)
    rsh.ipList_start(rsh.ipList)
    logger.info(u'快速执行脚本 %s, 创建作业实例目标机器 %s' % (nmScript.name, data['ipList']))
    ret = rsh.run_job(rsh.target)
    logger.info(u'快速执行脚本 %s, 执行结果 %s' % (nmScript.name, ret))
    rsh.stepInstance_end()
    logger.info(u'快速执行脚本 %s, 步骤示例保存完成' % nmScript.name)
    is_error = rsh.save_ret(ret)
    logger.info(u'快速执行脚本 %s, 保存作业步骤实例执行结果' % nmScript.name)
    rsh.save_status(is_error)
    logger.info(u'快速执行脚本 %s, 保存作业步骤实例例执行状态：%s' % (nmScript.name, is_error))
    nmInstance.end()
    logger.info(u'快速执行脚本 %s, 作业实例保存完成' % nmScript.name)
    nmInstance.save_status(is_error)
    logger.info(u'快速执行脚本 %s, 作业实例状态保存完成，状态: %s' % (nmScript.name, is_error))


@login_required
def fastPushfile(request):
    # 首页
    return render_to_response('job/fastPushfile.html', locals(), context_instance=RequestContext(request))


@login_required
def fastPushfile_upload_file(request):
    # 上传分发文件
    fileobj = request.FILES.get('file', None)
    content = fileobj.readlines()
    with open('%s%s' % (UPLOAD_FILE_DIR, fileobj.name), 'a+') as f:
        f.writelines(content)
    response = HttpResponse()
    response.write(json.dumps('ok'))
    return response


@login_required
@verification(Check_fastPushfile)
def run_fastPushfile(request):
    # 异步运行快速分发文件任务
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    data['operator'] = cur.nowuser.username
    run_fastPushfile_async(data)
    # run_fastPushfile_async.delay(data)
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': [u'操作成功']}))
    return response


class PushFileHelp(RunTaskHelp):
    """
    传送文件帮助
    """
    def __init__(self, data):
        super(PushFileHelp, self).__init__(data)

        self.fileTargetPath = data.get('fileTargetPath', '')
        # 目标路径最后一位如果没有反斜线 /，那么就加一个
        if not self.fileTargetPath.rfind('/') == (len(self.fileTargetPath) - 1):
            self.fileTargetPath += '/'

    def run_job(self, target, fileSource):
        # 执行作业
        rets = {}
        for file in fileSource:
            ret = self.saltH.run_fastPushfile(target,
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
            strVal = str(v)
            if k in rets:
                rets[k] = rets[k] + '\n' + strVal
            else:
                rets[k] = strVal

    def save_ret(self, rets):
        # 保存结果，错误判断 is_error
        server_help = Server_Help()
        servers = server_help.get_servers_dict1()
        for key, val in rets.items():
            if key not in servers:
                logger.error(u'主机名错误 %s %s' % (key, servers))
                continue
            ipList = Nm_StepInstanceIpList.objects.get(stepInstance_id=self.step_instance, ip=servers[key])
            ipList.result = u'文件推送结果 ' + val
            ipList.save()

    def check_status(self, target, fileSource):
        # 利用md5检测传输文件是否成功，有一个失败，那么任务就算失败
        status = True # 检测状态 True 成功 False 失败
        server_help = Server_Help()
        servers = server_help.get_servers_dict1()
        for file in fileSource:
            # 获取源文件的md5值
            md5, t = self.saltH.get_file_md5(file['name'])
            # 检测目标文件md5值
            ret = self.saltH.check_file_md5(target,
                                        file['name'],
                                        self.fileTargetPath, md5)

            for hostname, val in ret.items():
                if isinstance(val, bool):
                    if not val:
                        status = False
                else:
                    msg = u"检测文件 '%s' md5值时异常，路径：%s 目标机器:%s，内容:%s" % \
                           (file['name'], self.fileTargetPath, hostname, val)
                    status = False
                    logger.error(msg)

                if hostname not in servers:
                    logger.error(u'主机名错误 %s %s' % (hostname, servers))
                    continue
                ipList = Nm_StepInstanceIpList.objects.get(stepInstance_id=self.step_instance, ip=servers[hostname])
                md5CheckResult = [u'\n检测 %s 文件md5 ' % file['name'], u'结果:%s' % val, u' 状态:%s' % status]
                ipList.result += ''.join(md5CheckResult)
                ipList.save()

        return status


class FastPushFileHelp(PushFileHelp):
    """
    快速传送文件帮助
    """
    def __init__(self, data):
        super(FastPushFileHelp, self).__init__(data)
        self.taskName = data.get('task_name', '')
        self.ipList = data.get('ipList', '')
        self.target = self.saltH.getTarget(self.ipList)
        self.fileSource = data.get('fileSource', '')

    def stepInstance_start(self, instance):
        # 作业实例步骤 start
        self.step_instance.taskInstanceId = instance
        self.step_instance.name = self.taskName
        self.step_instance.type = 2
        self.step_instance.ord = 1
        self.step_instance.blockOrd = 1
        self.step_instance.blockName = self.taskName
        self.step_instance.account = self.account
        self.step_instance.fileSource = json.dumps(self.fileSource)
        self.step_instance.fileTargetPath = self.fileTargetPath
        self.step_instance.scriptTimeout = self.scriptTimeout
        self.step_instance.operator = self.operator
        self.step_instance.status = 2
        self.step_instance.startTime = self.dt.now_time
        self.step_instance.save()


@shared_task()
def run_fastPushfile_async(data):
    # 异步推送文件
    rsh = FastPushFileHelp(data)
    nmInstance = NmInstanceHelp(data['task_name'], data['operator'])
    nmInstance.start()
    logger.info(u'快速传输文件，作业名称：%s, 创建作业实例' % data['task_name'])
    rsh.stepInstance_start(nmInstance.instance)
    logger.info(u'快速传输文件，作业名称：%s, 创建作业步骤实例' % data['task_name'])
    rsh.ipList_start(rsh.ipList)
    logger.info(u'快速传输文件，作业名称：%s, 创建作业目标机器实例 %s' % (data['task_name'], data['ipList']))
    rets = rsh.run_job(rsh.target, rsh.fileSource)
    files = [f['name'] for f in data['fileSource']]
    logger.info(u'快速传输文件，作业名称：%s, 传输文件 %s' % (data['task_name'], files))
    nmInstance.end()
    logger.info(u'快速传输文件，作业名称：%s, 保存作业实例时间' % data['task_name'])
    rsh.stepInstance_end()
    logger.info(u'快速传输文件，作业名称：%s, 保存作业步骤实例时间' % data['task_name'])
    rsh.save_ret(rets)
    logger.info(u'快速传输文件，作业名称：%s, 保存执行结果 %s' % (data['task_name'], rets))
    is_error = rsh.check_status(rsh.target, rsh.fileSource)
    rsh.save_status(is_error)
    logger.info(u'快速传输文件，作业名称：%s, 保存步骤实例执行状态 %s' % (data['task_name'], is_error))
    nmInstance.save_status(is_error)
    logger.info(u'快速传输文件，作业名称：%s, 保存作业实例执行状态 %s' % (data['task_name'], is_error))

