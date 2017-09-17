# -*- coding: UTF-8 -*-
from django.test import TestCase

# Create your tests here.

import salt.client

client = salt.client.LocalClient()

# ret = client.cmd('blueking_test', 'cmd.script', ['salt://test.sh'])
ret = client.cmd('*', 'cp.get_file', ['/srv/salt/upload_file/bootstrap-table-develop.zip', '/tmp/bootstrap-table-develop.zip'])
#cmd内格式：'<操作目标>','<模块>','[参数]'。例：'*','cmd.run',['df -h']

print ret


