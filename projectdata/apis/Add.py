#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function

__author__ = 'xuebk'
from AppCode.api.projectdata import models
import yaml
import json

dir_logs = '/Users/xuebaoku/Documents/YGZX/AppCode/DevOps_ProjectAdmin/AppCode/api/projectdata/apis'
# dir_logs = '/data/service/devops/devops_projectadmin/AppCode/api/projectdata/apis'

def _get_Configurations():
    """
    获得默认默认 yaml 文件配置
    :return:
    """
    _return = {}
    _file = None
    try:
        _file = open('%s/application.yml' % dir_logs, 'r')
        _return = yaml.load(_file)
        if len(_return) == 0:
            raise Exception(u'文件为空')
    except Exception as e:
        print(e)
    finally:
        if _file:
            _file.close()
    return _return

data = _get_Configurations()

for k, v in data.items():
    for key, app in v['Applications'].items():
        models.Applications.objects.create(
            name=app['name'],
            code=app['code'],
            note='',
            HostsData=json.dumps(app['HostsData']),
            AppData=json.dumps(app['AppData']),
        )


models.Projects.objects.create(
    name='借款端',
    code='loan_online',
)
models.Projects.objects.create(
    name='普城信审',
    code='xspt',
)
models.Projects.objects.create(
    name='债券匹配',
    code='zqpp',
)
models.Projects.objects.create(
    name='银谷在线',
    code='YGZX',
)
for k, v in data.items():
    codes = models.Projects.objects.get(code=v['code'])
    for key, app in v['Applications'].items():
        codes.Applications.add(
            models.Applications.objects.get(code=app['code'])
        )
