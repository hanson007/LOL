#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import copy
import json
from django.db import models
# django 的时间.模块
from django.utils import timezone
# mptt 给前台的菜单所需
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.contrib import admin

logger = logging.getLogger(__name__)
DICT_NULL_BLANK_TRUE = {
    # 默认demols 状态
    'null': True,
    'blank': True
}


class UsableStatus(object):
    """
    默认状态
    """
    UNUSABLE = 0
    USABLE = 1
    DELETED = 99
    STATUS = (
        (UNUSABLE, u'禁用'),
        (USABLE, u'启用'),
        (DELETED, u'删除'),
    )


class EnvIronMent(models.Model):
    """
        操作方法
    """
    name = models.CharField(
        u'名称', max_length=50
    )
    code = models.CharField(
        u'标识符', max_length=50, unique=True
    )
    note = models.TextField(
        '备注',
        **DICT_NULL_BLANK_TRUE
    )

    def __unicode__(self):
        return u'code:%s name:%s' % (
            self.code, self.name
        )

    class Meta:
        verbose_name = u'系统发布-环境'
        verbose_name_plural = u"系统发布-环境"


class Applications(models.Model):
    """
        应用方法
    """
    name = models.CharField(
        u'名称', max_length=50
    )
    code = models.CharField(
        u'标识符', max_length=50, unique=True
    )
    note = models.TextField(
        '备注',
        help_text='标准备注啊',
        **DICT_NULL_BLANK_TRUE
    )
    HostsData = models.TextField(
        '主机列表',
        help_text='主机列表,请存贮list列表',
        **DICT_NULL_BLANK_TRUE
    )
    AppData = models.TextField(
        '基础数据集合',
        help_text='基础数据集合,请存贮dict字典',
        **DICT_NULL_BLANK_TRUE
    )

    def __unicode__(self):
        return u'code:%s name:%s' % (
            self.code, self.name
        )

    class Meta:
        verbose_name = u'系统发布-应用'
        verbose_name_plural = u"系统发布-应用"


class Projects(models.Model):
    name = models.CharField(
        u'项目名称', max_length=50
    )
    code = models.CharField(
        u'标识符', max_length=50, unique=True
    )
    EnvIronMent = models.ManyToManyField(
        EnvIronMent,
        verbose_name=u"环境关联",
        **DICT_NULL_BLANK_TRUE
    )
    Applications = models.ManyToManyField(
        Applications,
        verbose_name=u"应用关联",
        **DICT_NULL_BLANK_TRUE
    )
    createTime = models.DateTimeField(
        verbose_name=u"数据创建时间",
        default=timezone.now
    )
    updateTime = models.DateTimeField(
        verbose_name=u"数据更新时间",
        default=timezone.now
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'系统发布-项目'
        verbose_name_plural = u"系统发布-项目"

