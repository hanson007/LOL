# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Account(models.Model):
    # 账户
    name = models.CharField(max_length=255, null=True, unique=True, verbose_name=u'账户名称')
    desc = models.CharField(max_length=255, null=True, verbose_name=u'描述')
    creater = models.CharField(max_length=255, null=True, verbose_name=u'创建人')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    ModifyUser = models.CharField(max_length=255, null=True, verbose_name=u'修改人')
    ModifyTime = models.DateTimeField(null=True, auto_now=True, verbose_name=u'修改时间')

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.desc, self.ModifyTime)

    class Meta:
        db_table = 'account'
        permissions = (
            ("view_account", u'查看账户'),
            ("edit_account", u'编辑账户'),
        )


class Nm_Script(models.Model):
    # 脚本
    name = models.CharField(max_length=255, null=True, unique=True, verbose_name=u'名称')
    appId = models.CharField(max_length=255, null=True, verbose_name=u'开发商id')
    # '类型:1(shell脚本)、2(bat脚本)、3(perl脚本)、4(python脚本)'
    TYPE = models.IntegerField(blank=True, null=True, default=1, verbose_name=u'类型')
    # '是否公共脚本,0.否 1.是'
    isPublic = models.BooleanField(default=True, verbose_name=u'是否公共脚本')
    content = models.TextField(blank=True, null=True, verbose_name=u'脚本内容')
    creater = models.CharField(max_length=255, null=True, verbose_name=u'创建人')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    ModifyUser = models.CharField(max_length=255, null=True, verbose_name=u'修改人')
    ModifyTime = models.DateTimeField(null=True, auto_now=True, verbose_name=u'修改时间')

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.TYPE, self.ModifyTime)

    class Meta:
        db_table = 'nm_script'
        permissions = (
            ("view_script", u'查看脚本'),
            ("edit_script", u'编辑脚本'),
        )
