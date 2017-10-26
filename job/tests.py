# -*- coding: UTF-8 -*-
from django.test import TestCase

# Create your tests here.

import salt.client

client = salt.client.LocalClient()

ret = client.cmd('*', 'user.list_users', tgt_type='compound')
print ret
# ret = client.cmd('*', 'cmd.script', ['salt://test.sh'])
# ret = client.cmd('*', 'file.file_exists', ['/tmp/bootstrap-table-develop.zip'], tgt_type='compound')
# ret = client.cmd('*', 'cp.get_file', ['salt://upload_file/bootstrap-table-develop.zip', '/tmp/bootstrap-table-develop.zip'])
#cmd内格式：'<操作目标>','<模块>','[参数]'。例：'*','cmd.run',['df -h']

# print ret

# dict1 = {'a': 'test1', 'b': 'test2'}
# dict2 = {'a': 'test1_dict2', 'b': 'test2_dict2'}
# dict1 = {'a': True, 'b': True}
# dict2 = {'a': True, 'b': False}
# print dict1.values()
# total = [dict1, dict2]
#
#
# def test(rets, ret):
#     for k, v in ret.items():
#         if k in rets:
#             rets[k].append(v)
#         else:
#             rets[k] = [v]
#
# rets = {}
# for ret in total:
#     test(rets, ret)

# print rets
# ret = dict2.values()
# print all(ret)
# a = '/tmp/backup/'
# print a.rfind('/') == (len(a) - 1), list(a)

