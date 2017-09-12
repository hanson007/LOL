# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from job.models import *
from controller.core.public import *
import json
# Create your views here.


@login_required
def taskInstanceList(request):
    # 首页
    return render_to_response('log_record/taskInstansList.html', locals(), context_instance=RequestContext(request))


@login_required
def get_taskInstance(request):
    # 获取任务实例列表
    data = Nm_Instance.objects.all().values()
    cur = Currency(request)
    data_str = [transfor(d) for d in data]
    print data_str
    response = HttpResponse()
    response.write(json.dumps(data_str))
    return response


def transfor(d):
    status_list = {3: u'执行成功', 4: u'执行失败', 2: u'正在执行'}
    dict1 = {}
    for k, v in d.items():
        if isinstance(v, datetime.datetime):
            v = v.strftime("%Y-%m-%d %H:%M:%S")
        dict1[k] = v
        if k == 'status':
            dict1[k] = status_list[v]

    return dict1