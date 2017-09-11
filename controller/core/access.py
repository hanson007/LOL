# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月07日
# Company:          东方银谷
from public import *
from business.models import *
from cmdb.models import Server
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
        self.account = data.get('account', '')
        self.content = data.get('content', '')
        self.ipList = data.get('ipList', [])
        self.scriptParam = data.get('scriptParam', '')
        self.scriptTimeout = data.get('scriptTimeout', '')
        self.script_type = data.get('script_type', '')

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

    def check_script_type(self):
        # 检测脚本类型
        if self.script_type not in ['shell', 'python']:
            self.error_msg.append(u'脚本类型错误')

    def check_script_timeout(self):
        # 检测脚本超时时间
        if not self.scriptTimeout:
            self.error_msg.append(u'超时时间不能为空')
        else:
            if not self.scriptTimeout.isdecimal():
                self.error_msg.append(u'超时时间必须为十进制数')

    def total_check(self):
        self.check_script_name()
        self.check_account()
        self.check_content()
        self.check_ipList()
        self.check_script_type()
        self.check_script_timeout()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Check_Mod_Periodic_Task(Check_Task):
    """
    检测修改周期任务提交的信息
    """
    def __init__(self, request):
        super(Check_Mod_Periodic_Task, self).__init__(request)
        self.task_id = self.data.get('_id', '')

    # def check_task_name(self):
    #     # 检测任务名称
    #     if not self.task_name:
    #         self.error_msg.append(u'任务名称不能为空')
    #     else:
    #         Q_like = ~Q(id=int(self.task_id)) & Q(name=self.task_name)
    #         is_have = PeriodicTask.objects.filter(Q_like).exists()
    #         if is_have:
    #             self.error_msg.append(u'任务名称已存在')

    def check_task_id(self):
        # 检测任务ID
        if not self.task_id:
            self.error_msg.append(u'任务ID不能为空')
        else:
            is_have = PeriodicTask.objects.filter(pk=int(self.task_id)).exists()
            if not is_have:
                self.error_msg.append(u'任务ID不存在')

    def total_check(self):
        self.check_task_name()
        # self.check_task_template()
        self.check_is_enable()
        self.check_is_encrypt()
        self.check_mail_header()
        self.check_receivers_cc()
        # self.check_crontab()
        self.check_sql_list()
        self.check_task_id()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Server_Help(object):
    def __init__(self):
        pass

    def get_servers_dict(self):
        # 获取作业实例目标机器，字典格式
        servers_data = Server.objects.all().values()
        servers = {}
        for dt in servers_data:
            servers[dt['hostname']] = dt['ip']
        return servers