# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月07日
# Company:          东方银谷
from public import *
from business.models import *
from cmdb.models import *
from job.models import *
from salt_operation import Salt_Help
from django.http import HttpResponse
from functools import wraps
import json


def verification(check_class):
    """
    装饰器用于检测用户提交的信息是否合法.
    check_class 检测类
    Decorator for views that checks that the user submitted information,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = HttpResponse()
            ccl = check_class(request)
            check_status, error_msg = ccl.total_check()
            if check_status:
                response.write(json.dumps({'status': check_status, 'msg': error_msg}))
                return response

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class Check_Task(object):
    """
    检测新增周期任务提交的信息
    error_msg 存放所有错误消息
    check_status 错误状态 1 错误，0 正常，主要用于前端的JavaScript进行判断
    total_check 启动所有检测，返回检测状态和错误消息
    """
    def __init__(self, request):
        cur = Currency(request)
        rq_post = getattr(cur, 'rq_post')
        jdata = rq_post('data')
        data = json.loads(jdata)
        self.data = data
        self.error_msg = []
        self.script_name = data.get('script_name', '')
        self.script_id = data.get('script_id', '')
        self.account = data.get('account', '')
        self.content = data.get('content', '')
        self.ipList = data.get('ipList', [])
        self.scriptParam = data.get('scriptParam', '')
        self.scriptTimeout = data.get('scriptTimeout', '')
        self.script_type = data.get('script_type', '')
        self.saltH = Salt_Help()

    def check_script_id(self):
        # 检测脚本id
        if not self.script_id or not str(self.script_id).isdigit():
            self.error_msg.append(u'请选择脚本')
        else:
            if not Nm_Script.objects.filter(pk=int(self.script_id)):
                self.error_msg.append(u'脚本不存在')

    def check_script_name(self):
        # 检测脚本名称
        if not self.script_name:
            self.error_msg.append(u'脚本名称不能为空')

    def check_account(self):
        # 检测运行账号
        if not self.account:
            self.error_msg.append(u'账号名称不能为空')
        else:
            is_have = Account.objects.filter(name=self.account).exists()
            if not is_have:
                self.error_msg.append(u'账号名称不存在')

    def check_content(self):
        # 检测脚本内容
        if not self.content:
            self.error_msg.append(u'脚本内容不能为空')

    def check_ipList(self):
        # 检测需要运行脚本的服务器
        if not isinstance(self.ipList, list):
            self.error_msg.append(u'提交的服务器不是一个列表')
        else:
            if not self.ipList:
                self.error_msg.append(u'至少选择一台服务器')
            else:
                not_exists = [ip for ip in self.ipList if not Server.objects.filter(ip=ip).exists()]
                if not_exists:
                    self.error_msg.append(u'%s 不存在' % ','.join(not_exists))
                else:
                    # 如果提交IP在cmdb里，则通过salt检测连通性
                    self.test_ping()

    def check_script_type(self):
        # 检测脚本类型
        if self.script_type not in ['1', '4']:
            self.error_msg.append(u'脚本类型错误')

    def check_script_timeout(self):
        # 检测脚本超时时间
        if not self.scriptTimeout:
            self.error_msg.append(u'超时时间不能为空')
        else:
            if not self.scriptTimeout.isdecimal():
                self.error_msg.append(u'超时时间必须为十进制数')

    def test_ping(self):
        """
        检测ip是否能够ping通(ipList里的IP肯定存在,已检测过.)
        :param ipList:
        :return:
        """
        target = self.saltH.getTarget(self.ipList)
        rets = self.saltH.test_ping(target)
        server_help = Server_Help()
        servers = server_help.get_servers_dict2()
        errorIp = []
        errorPing = []
        for ip in self.ipList:
            hostname = servers[ip]
            if hostname not in rets:
                errorIp.append(ip)
            else:
                if not rets[hostname]:
                    errorPing.append(ip)

        if errorIp:
            msg = u'服务器：%s，ip或主机名错误.' % '、'.join(errorIp)
            self.error_msg.append(msg)
        if errorPing:
            msg = u'salt master无法ping通%s.' % '、'.join(errorPing)
            self.error_msg.append(msg)

    def total_check(self):
        self.check_script_id()
        self.check_account()
        self.check_ipList()
        self.check_script_timeout()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Check_fastPushfile(Check_Task):
    """
    检测修改周期任务提交的信息
    """
    def __init__(self, request):
        super(Check_fastPushfile, self).__init__(request)
        self.task_name = self.data.get('task_name', '')
        self.fileSource = self.data.get('fileSource', [])
        self.fileTargetPath = self.data.get('fileTargetPath', '')

    def check_task_name(self):
        # 检测任务名称
        if not self.task_name:
            self.error_msg.append(u'任务名称不能为空')

    def check_fileSource(self):
        # 检测任务名称
        if not self.fileSource:
            self.error_msg.append(u'上传文件不能为空')

    def check_fileTargetPath(self):
        # 检测任务名称
        if not self.fileTargetPath:
            self.error_msg.append(u'目标路径不能为空')

    def total_check(self):
        self.check_task_name()
        self.check_fileSource()
        self.check_fileTargetPath()
        self.check_account()
        self.check_ipList()
        self.check_script_timeout()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Server_Help(object):
    def __init__(self):
        self.data = Server.objects.all().values()

    def get_servers_dict1(self):
        # 获取作业实例目标机器，字典格式
        servers = {}
        for dt in self.data:
            servers[dt['hostname']] = dt['ip']
        return servers

    def get_servers_dict2(self):
        # 获取作业实例目标机器，字典格式
        servers = {}
        for dt in self.data:
            servers[dt['ip']] = dt['hostname']
        return servers


class Check_AddScript(Check_Task):
    """
    检测新增脚本信息
    """
    def __init__(self, request):
        super(Check_AddScript, self).__init__(request)

    def check_script_name(self):
        # 检测脚本名称
        if not self.script_name:
            self.error_msg.append(u'脚本名称不能为空')
        if Nm_Script.objects.filter(name=self.script_name).exists():
            self.error_msg.append(u'脚本名称已存在')

    def total_check(self):
        self.check_script_name()
        self.check_content()
        self.check_script_type()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Check_EditScript(Check_AddScript):
    """
    检测需要编辑的脚本信息
    """
    def __init__(self, request):
        super(Check_EditScript, self).__init__(request)

    def check_script_name(self):
        # 检测脚本名称
        if not self.script_name:
            self.error_msg.append(u'脚本名称不能为空')
        if Nm_Script.objects.filter(name=self.script_name).exclude(pk=int(self.script_id)).exists():
            self.error_msg.append(u'脚本名称已存在')


class CheckNewTask(object):
    def __init__(self, request):
        cur = Currency(request)
        rq_post = getattr(cur, 'rq_post')
        jdata = rq_post('data')
        data = json.loads(jdata)
        self.nm_step = data.get('nm_step', [])
        self.data = data
        self.error_msg = []
        self.nm_task = data.get('nm_task', {})

    def checkTaskName(self):
        # 作业名称不能为空
        taskName = self.nm_task.get('taskName', {})
        if not taskName:
            self.error_msg.append(u'作业名称不能为空')
        else:
            if Nm_Task.objects.filter(name=taskName).exists():
                self.error_msg.append(u'作业名称已存在')

    def checkTaskStep(self):
        if not self.nm_step:
            self.error_msg.append(u'新建作业至少包含一个步骤')
        else:
            for ordData in self.nm_step:
                self.checkOrd(ordData)

    def checkOrd(self, ordData):
        blockName = ordData.get('blockName', '')
        blockOrd = ordData.get('blockOrd', 1)
        ord = ordData.get('ord', 1)
        account = ordData.get('account', '')
        scriptTimeout = ordData.get('scriptTimeout', '')
        ipList = ordData.get('ipList', [])
        stepType = ordData.get('type', 0)

        scriptId = ordData.get('scriptId', 0)
        scriptParam = ordData.get('scriptParam', '')

        fileSource = ordData.get('fileSource', [])
        fileTargetPath = ordData.get('fileTargetPath', '')

        if stepType not in (1, 2):
            self.error_msg.append(u'步骤%s,节点%s的 步骤类型 错误' % (blockOrd, ord))
            return

        if not blockName:
            self.error_msg.append(u'步骤%s,节点%s的 步骤名称 不能为空' % (blockOrd, ord))

        if not account:
            self.error_msg.append(u'步骤%s,节点%s的 账号 不能为空' % (blockOrd, ord))

        if not ipList:
            self.error_msg.append(u'步骤%s,节点%s的 目标机器 不能为空' % (blockOrd, ord))
        else:
            for _id in ipList:
                if not Server.objects.filter(pk=int(_id)):
                    self.error_msg.append(u'步骤%s,节点%s的 目标机器 不存在' % (blockOrd, ord))

        if not scriptTimeout or not scriptTimeout.isdigit():
            self.error_msg.append(u'步骤%s,节点%s的 超时时间 不能为空且必须为数字' % (blockOrd, ord))

        if stepType == 1:  # 执行脚本
            if not scriptId:
                self.error_msg.append(u'步骤%s,节点%s的 脚本 不能为空' % (blockOrd, ord))
            else:
                if not Nm_Script.objects.filter(pk=int(scriptId)).exists():
                    self.error_msg.append(u'步骤%s,节点%s的 脚本 不存在' % (blockOrd, ord))

        if stepType == 2:  # 传送文件
            if not fileSource:
                self.error_msg.append(u'步骤%s,节点%s的 文件 不能为空' % (blockOrd, ord))

            if not fileTargetPath:
                self.error_msg.append(u'步骤%s,节点%s的 目标路径 不能为空' % (blockOrd, ord))

    def total_check(self):
        self.checkTaskName()
        self.checkTaskStep()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class CheckEditTask(CheckNewTask):
    def __init__(self, request):
        super(CheckEditTask, self).__init__(request)

    def checkTaskName(self):
        # 作业名称不能为空
        taskName = self.nm_task.get('taskName', {})
        if not taskName:
            self.error_msg.append(u'作业名称不能为空')

    def checkTaskId(self):
        taskId = self.nm_task.get('taskId', '')
        if not Nm_Task.objects.filter(pk=int(taskId)):
            self.error_msg.append(u'作业ID不存在')

    def total_check(self):
        self.checkTaskName()
        self.checkTaskId()
        self.checkTaskStep()
        status = 1 if self.error_msg else 0

        return status, self.error_msg