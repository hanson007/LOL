# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from controller.core.public import *
from controller.core.access import (Check_Task, verification)
from models import *
from business.models import Account
from django.shortcuts import render
from django.contrib import auth
import salt.client
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Create your views here.
@login_required
def script(request):
    # 首页
    return render_to_response('job/run_script.html', locals(), context_instance=RequestContext(request))


@login_required
# @verification(Check_Task)
def run_script(request):
    cur = Currency(request)
    jdata = cur.rq_post('data')
    data = json.loads(jdata)
    if os.path.isfile('/srv/salt/test.sh'):
        os.remove('/srv/salt/test.sh')
    cur.write_file('/srv/salt/test.sh', data['content'].split('\n'))
    client = salt.client.LocalClient()
    ret = client.cmd('*', 'cmd.script', ['salt://test.sh', 'runas=huangxiaoxue'])
    response = HttpResponse()
    response.write(json.dumps({'status': 0, 'msg': ['操作成功']}))
    return response
