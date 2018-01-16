#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)
import functools
import warnings
# rest_framework url 相关
import json
import os
import jinja2
from rest_framework.views import APIView
from rest_framework.renderers import *
from rest_framework.response import Response
from AppCode.api.Base import JsonResponse, get_parameter_dic, LogsFunc
from .models import Applications, EnvIronMent, Projects, models
import pprint
from django.http.response import HttpResponse
from django.conf import settings

Confs_templates = os.path.join(settings.BASE_DIR, 'AppCode/api/projectdata/apis/updata_app/templates'),


def DocParam(name="default", location="query",
             required=True, description=None, type="string",
             *args, **kwargs):
    return coreapi.Field(name=name, location=location,
                         required=required, description=description,
                         type=type)


class MyGetData(object):
    def __init__(self, request, RecordId, *args, **kwargs):
        self.request = request
        self.RecordId = RecordId

    def check_params(self):
        """
            检测 传入参数是否正常
        :param request:
        :param obj:
        :return:
        """
        logger.debug(u'唯一id: %s 当前方法:%s' % (self.RecordId, "check_params"))
        params = get_parameter_dic(self.request)
        try:
            data = EnvIronMent.objects.get(
                code=params['Env']
            ).projects_set.get(
                code=params['Projects']
            ).Applications.get(
                code=params['App']
            )
            return data, params
        except Exception:
            logger.debug(u'唯一id: %s 当前方法:%s 查询错误' % (self.RecordId, "check_params"))
            raise Exception(u'唯一id: %s 当前方法:%s 查询错误' % (self.RecordId, "check_params"))

    def get(self):
        """
        处理返回数据
        :return:
        """
        data, params = self.check_params()
        try:
            HostsData = json.loads(data.HostsData)
            AppData = json.loads(data.AppData)
        except Exception as e:
            print e.message
            raise Exception(u'原始数据错误!!')
        HostCheck = True
        try:
            for host in HostsData[params['Env']]:
                if unicode(host) == unicode(params['Host']):
                    HostCheck = False
        except Exception as e:
            print e.message
            raise Exception(u'原始数据错误!! >>> 解析主机ip地址有误')
        if HostCheck:
            raise Exception(u'此App没有这个主机!!')

        return AppData


class MyGetShell(MyGetData):
    def get(self):
        """
        处理返回数据
        :return:
        """
        AppData = super(MyGetShell, self).get()
        params = get_parameter_dic(self.request)
        params['data'] = AppData
        # 配置模板文件搜索路径
        TemplateLoader = jinja2.FileSystemLoader(searchpath=Confs_templates)
        # 创建环境变量
        TemplateEnv = jinja2.Environment(loader=TemplateLoader)

        # 加载模板，渲染数据
        template = TemplateEnv.get_template("git_pull.sh")
        html = template.render(params)
        return html


class GetData(APIView):
    """
        按照主机.获取应用相关信息
    """
    coreapi_fields = (
        DocParam("Env", description="环境信息"),
        DocParam("Host", description="主机信息."),
        DocParam("Projects", description="项目信息"),
        DocParam("App", description="应用信息"),
    )

    @LogsFunc()
    def get(self, request, RecordId, *args, **kwargs):
        rets = MyGetData(request, RecordId, *args, **kwargs)
        data = {
            'code': 200,
            'message': u'获取成功!',
            'results': rets.get()
        }
        return HttpResponse(data)


class get_shell(APIView):
    """
        按照主机.获取应用相关信息
    """
    coreapi_fields = (
        DocParam("Env", description="环境信息"),
        DocParam("Host", description="主机信息."),
        DocParam("Projects", description="项目信息"),
        DocParam("App", description="应用信息"),
        DocParam("commit_id", description="Git版本号")
    )

    @LogsFunc()
    def get(self, request, RecordId, *args, **kwargs):
        rets = MyGetShell(request, RecordId, *args, **kwargs)
        data = {
            'code': 200,
            'message': u'获取成功!',
            'results': rets.get()
        }
        return Response(rets.get())


def main():
    AppData = {
        'BIN_DIR': "/data/service/loan_online/${Name}",
        'CODE_DIR': "webapps/lo-server",
        'Bin_Start': "sh ./bin/startup.sh ",
        'Bin_Stop': "sh ./bin/StopTomcat.sh ",
        'Bin_Config': "sh ./bin/config.sh",
        'giturl': "http://YgzxReadOnly:vIa3hiar7eY0queG@git.yingu.com/YGZX/loan_online_loan_server.git",
    }

    Application = {
        'name': 'loan_server',
        'code': 'loan_server',
        'HostsData': ["172.16.3.20", "172.16.3.21"],
        'AppData': AppData,
    }
    ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    # 设定 commitid
    Name = "loan-consumer_2"
    BIN_DIR = "/data/service/loan_online/${Name}"
    CODE_DIR = ""
    Bin_Start = "sh start.sh"
    Bin_Stop = "sh stop.sh"
    Bin_Config = "echo 'ok'"
    giturl = "http://YgzxReadOnly:vIa3hiar7eY0queG@git.yingu.com/YGZX/loan-consumer.git"


if __name__ == '__main__':
    main()
