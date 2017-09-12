#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月09日
# Company:          东方银谷

import os
import salt.client
from public import *


class Salt_Help(object):
    # salt 通用操作
    def __init__(self):
        self.dth = Datetime_help()
        self.write_file = getattr(Currency, 'write_file')

    def delete_old_file(self, file):
        # 删除原有的文件
        full_file = '/srv/salt/%s' % file
        if os.path.isfile(full_file):
            os.remove(full_file)

    @property
    def file(self):
        # 文件
        return self.dth.nowtimestrf3 + '.sh'

    def create_script_file(self, file, content):
        self.write_file('/srv/salt/%s' % file, content)

    def run_script(self, target, file, scriptParam, account, timeout):
        client = salt.client.LocalClient()
        ret = client.cmd(target, 'cmd.script',
                         ['salt://%s' % file, scriptParam, 'runas=%s' % account, 'timeout=%s' % timeout],
                         tgt_type='compound')
        return ret