#!/usr/bin/python env
# -*- coding: UTF-8 -*-
# Description:                    
# Author:           黄小雪
# Date:             2017年09月12日
# Company:          东方银谷

from __future__ import absolute_import
from celery import shared_task, task


@shared_task()
def add(x, y):
    print x + y
    return x + y


@shared_task()
def mul(x, y):
    print "%d * %d = %d" % (x, y, x * y)
    return x * y


@shared_task()
def sub(x, y):
    print "%d - %d = %d" % (x, y, x - y)
    return x - y


@task(ignore_result=True, max_retries=1, default_retry_delay=10)
def just_print():
    print "Print from celery task"


