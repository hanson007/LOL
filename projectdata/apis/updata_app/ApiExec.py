#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function

__author__ = 'xuebk'
import json
import logging
import jinja2
import lib.log
import Configuration as my_cf
import requests
import os

logger = logging.getLogger(__name__)

# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 配置层
Confs = {
    'Url': 'api/projectdata/get_data',
    "templates": my_cf.os.path.join(my_cf.BASE_DIR, 'lib_exec/updata_app/templates'),
    "file_shell": my_cf.os.path.join(my_cf.BASE_DIR, 'logs')
}


def my_http(*args, **kwargs):
    logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, kwargs['requrl'], '=' * 2, '=' * 25))
    try:
        res_data = requests.get(
            kwargs['requrl'],
            kwargs['post_data'],
            timeout=10
        )
        try:
            logger.debug(
                "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.json()))
            )
            return res_data.json()
        except:
            logger.debug(
                "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.text))
            )
            raise Exception('错误')
        logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, 'success', '=' * 2, '=' * 25))
    except Exception as e:
        logger.error("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, 'failure', '=' * 2, '=' * 25))


# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 逻辑层
# # 数据url判定与获取
def check_url(host):
    """
    数据url判定与获取
    :return:
    """
    if host == 'dopa.yingujr.com':
        _urlhost = host
    else:
        _urlhost = 'dopa.yingujr.com'
    url = "http://%s/%s" % (_urlhost, Confs['Url'])
    return url


# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# 应用层
# # 获取基础数据
def get_app_data(*args, **kwargs):
    """
        获取应用基础信息
    :param args:
    :param kwargs:
    :return:
    """
    url = check_url(host=kwargs['Host'])
    __data = my_http(requrl=url, post_data={
        "Env": kwargs['Env'],
        "Host": kwargs['Host'],
        "Projects": kwargs['Projects'],
        "App": kwargs['App'],
    })
    if __data['code'] != 200:
        raise Exception(u'数据获取错误')
    return __data['results']


def updata(*args, **kwargs):
    """
        更新
    :param args:
    :param kwargs:
    :return:
    """
    if kwargs['commit_id'] == None:
        filename = 'git_pull.sh'
    else:
        filename = 'git_rev_parse.sh'
    # 配置模板文件搜索路径
    TemplateLoader = jinja2.FileSystemLoader(searchpath=Confs['templates'])

    # 创建环境变量
    TemplateEnv = jinja2.Environment(loader=TemplateLoader)

    # 加载模板，渲染数据
    template = TemplateEnv.get_template(filename)
    html = template.render(**kwargs)
    # 写入 临时文件中
    file_name = '%s/%s' %(Confs['file_shell'], filename)
    files = file(file_name, 'w')
    files.write(html)
    files.close()
    os.popen('/bin/bash %s' % file_name)


# #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
def demo(*args, **kwargs):
    """
        Oss 批量上传
    :param args:
    :param kwargs:
    :return:
    """
    # #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    # 传参处理
    parser = args[0]
    parser.add_argument("-projects", help="项目名称", default=None)
    parser.add_argument("-app", help="应用名称", default=None)
    parser.add_argument("-commit_id", help="git中commit_id", default=None)
    __args = parser.parse_args()
    if __args.app == None:
        parser.error(u'必须指定 项目名称')
    if __args.projects == None:
        parser.error(u'必须指定 应用名称')
    # #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    # 获取基础参数
    _conf = {
        "Host": my_cf.configration['host_ip'],
        "Env": my_cf.configration['EnvIronMent'],
        "Projects": __args.projects,
        "App": __args.app,
        "commit_id": __args.commit_id,
    }
    # #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    # 进入基础逻辑
    _data = {
        'data': get_app_data(**_conf)
    }
    updata(**dict(_data, **_conf))


if __name__ == '__main__':
    demo()
