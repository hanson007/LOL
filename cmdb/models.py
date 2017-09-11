# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Server(models.Model):
    # 服务器
    ip = models.CharField(max_length=255, null=True, unique=True, verbose_name=u'服务器IP地址')
    hostname = models.CharField(max_length=255, null=True, verbose_name=u'主机名')
    desc = models.CharField(max_length=255, null=True, verbose_name=u'服务器描述')
    creater = models.CharField(max_length=255, null=True, verbose_name=u'创建人')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    ModifyUser = models.CharField(max_length=255, null=True, verbose_name=u'修改人')
    ModifyTime = models.DateTimeField(null=True, auto_now=True, verbose_name=u'修改时间')

    def __unicode__(self):
        return '%s - %s - %s' % (self.ip, self.hostname, self.desc)

    class Meta:
        db_table = 'server'
        permissions = (
            ("view_server", u'查看服务器'),
            ("edit_server", u'编辑服务器'),
        )
