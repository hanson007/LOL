#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月17日
# Company:          东方银谷

UPLOAD_FILE_DIR = '/srv/salt/upload_file/'
SALT_UPLOAD_FILE = 'salt://upload_file/'
MASTER = '192.168.190.130'

# 作业状态转换表
STATUS_TABLE = {
    1:u'未执行',
    2:u'正在执行',
    3:u'执行成功',
    4:u'执行失败',
    5:u'跳过',
    6:u'忽略错误',
    7:u'等待用户',
    8:u'手动结束',
    9:u'状态异常',
    10:u'步骤强制终止中',
    11:u'步骤强制终止成功',
    12:u'步骤强制终止失败',
}