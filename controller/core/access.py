# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月07日
# Company:          东方银谷
from public import *
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


class Check_Periodic_Task(object):
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
        self.script_type = data.get('script_type', '')

    # def check_task_name(self):
    #     # 检测任务名称
    #     if not self.task_name:
    #         self.error_msg.append(u'任务名称不能为空')
    #     else:
    #         is_have = PeriodicTask.objects.filter(name=self.task_name).exists()
    #         if is_have:
    #             self.error_msg.append(u'任务名称已存在')

    # def check_task_template(self):
    #     # 检测任务模板
    #     loaders.autodiscover()
    #     tasks = list(sorted(registry.tasks.regular().keys()))
    #
    #     if self.task_template:
    #         if self.task_template not in tasks:
    #             self.error_msg.append(u'任务模板不存在')
    #     else:
    #         self.error_msg.append(u'任务模板不能为空')

    # def check_is_enable(self):
    #     # 检测“是否启用”
    #     if not isinstance(self.is_enable, bool):
    #         self.error_msg.append(u'"是否启用" 值错误')
    #
    # def check_is_encrypt(self):
    #     # 检测“是否加密”
    #     if not isinstance(self.is_encrypt, bool):
    #         self.error_msg.append(u'"是否加密" 值错误')
    #
    # def check_mail_header(self):
    #     if not 0 < len(self.mail_header) < 30:
    #         self.error_msg.append(u'邮件标题不能为空或者超过30个字符')
    #
    # def check_receivers_cc(self):
    #     if not self.receivers and not self.cc:
    #         self.error_msg.append(u'收件人和抄送人不能全部为空')

    # def check_crontab(self):
    #     crons = CrontabSchedule.objects.values('id')
    #     try:
    #         if long(self.crontab) not in [c['id'] for c in crons]:
    #             self.error_msg.append(u'执行时间错误')
    #     except Exception, e:
    #         self.error_msg.append(u'执行时间错误')

    # def check_sql_list(self):
    #     if not self.sql_list:
    #         self.error_msg.append(u'SQL不能为空，至少包含一个SQL语句')
    #     else:
    #         for dt in self.sql_list:
    #             status = False
    #             if not dt['database']:
    #                 status = True
    #                 self.error_msg.append(u'%s SQL执行数据库不能为空' % (dt['sql_name']) )
    #             if not dt['sql']:
    #                 status = True
    #                 self.error_msg.append(u'%s SQL语句不能为空' % (dt['sql_name']))
    #             if not dt['sql_name']:
    #                 status = True
    #                 self.error_msg.append(u'SQL名称不能为空')
    #             if status:
    #                 break

    def total_check(self):
        # self.check_task_name()
        # self.check_task_template()
        # self.check_is_enable()
        # self.check_is_encrypt()
        # self.check_mail_header()
        # self.check_receivers_cc()
        # self.check_crontab()
        # self.check_sql_list()
        status = 1 if self.error_msg else 0

        return status, self.error_msg


class Check_Mod_Periodic_Task(Check_Periodic_Task):
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