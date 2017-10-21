#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月09日
# Company:          东方银谷

import os
import salt.client
from public import *
from controller.conf.job import *
import logging
logger = logging.getLogger('job')


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

    def run_fastPushfile(self, target, filename, fileTargetPath, account, timeout):
        client = salt.client.LocalClient()
        ret = client.cmd(target, 'cp.get_file',
                         ['%s%s' % (SALT_UPLOAD_FILE, filename),
                          '%s%s' % (fileTargetPath, filename),
                          'runas=%s' % account, 'timeout=%s' % timeout],
                         tgt_type='compound')
        return ret

    def check_file_md5(self, target, filename, fileTargetPath, md5):
        client = salt.client.LocalClient()
        ret = client.cmd(target, 'file.check_hash',
                         ['%s%s' % (fileTargetPath, filename), md5],
                         tgt_type='compound')
        return ret

    def get_file_md5(self, filename):
        client = salt.client.LocalClient()
        ret = client.cmd('S@%s' % MASTER, 'file.get_sum',
                         ['%s%s' % (UPLOAD_FILE_DIR, filename), 'md5'],
                         tgt_type='compound')
        if ret:
            md5 = ret.values()[0]
            status = True
        else:
            md5 = ''
            status = False
            logger.error(u"源文件 '%s' 的md5值获取失败，请检查上传目录、saltMaster服务器IP" % filename)
        return md5, status
