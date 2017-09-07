# -*- coding: UTF-8 -*-
from django.test import TestCase

# Create your tests here.

# import salt.client
#
# client = salt.client.LocalClient()
#
# ret = client.cmd('*', 'cmd.script', ['salt://test.sh'])
# #cmd内格式：'<操作目标>','<模块>','[参数]'。例：'*','cmd.run',['df -h']
#
# print ret
import sys
reload(sys)
sys.setdefaultencoding('utf8')

with open('test.sh', 'a+') as f:
    f.write('123')
    f.write(u'你好')
