# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from business.models import Nm_Script

# Create your models here.


class Nm_Instance(models.Model):
    # 作业实例

    # 执行作业id: -1 快速执行脚本
    taskId = models.IntegerField(null=True, verbose_name=u'执行作业id')
    appId = models.IntegerField(null=True, verbose_name=u'业务id')
    # # 快速执行脚本时，执行作业名称=脚本名称 + 时间
    name = models.CharField(max_length=255, null=True, verbose_name=u'作业名称')
    operator = models.CharField(max_length=255, null=True, verbose_name=u'执行人')
    # 启动方式： 1.页面执行、2.API调用、3.定时执行
    startWay = models.IntegerField(null=True, verbose_name=u'启动方式')
    currentStepId = models.IntegerField(null=True, verbose_name=u'当前执行步骤id')
    # 状态：1.未执行、2.正在执行、3.执行成功、4.执行失败、5.跳过、6.忽略错误、7.等待用户、
    #      8.手动结束、9.状态异常、10.步骤强制终止中、11.步骤强制终止成功、12.步骤强制终止失败
    status = models.IntegerField(null=True, default=1, verbose_name=u'状态')
    startTime = models.DateTimeField(null=True, verbose_name=u'开始时间')
    endTime = models.DateTimeField(null=True, verbose_name=u'结束时间')
    # # 总耗时，单位：秒
    totalTime = models.FloatField(max_length=11, null=True, default=False, verbose_name=u'总耗时')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    mobileTaskId = models.IntegerField(null=True, verbose_name=u'移动作业id')
    tagId = models.IntegerField(null=True, verbose_name=u'标签Id')

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.status, self.totalTime)

    class Meta:
        db_table = 'nm_instance'


class Nm_StepInstance(models.Model):
    """
    作业实例步骤
    块名称blockName相当于步骤名称，每一个步骤里又分许多小步骤，小步骤名称对应的是name
    blockOrd 大步骤的执行顺序，ord小步骤的执行顺序
    """
    # 执行作业id: -1 快速执行脚本
    stepId = models.IntegerField(null=True, verbose_name=u'执行步骤id')
    taskInstanceId = models.ForeignKey(Nm_Instance, related_name="nm_instance_set")
    appId = models.IntegerField(null=True, verbose_name=u'业务id')
    # 快速执行脚本时，节点名称=脚本名称 + 时间
    name = models.CharField(max_length=255, null=True, verbose_name=u'节点名称')
    # 步骤类型：1、执行脚本，2、传输文件，3、文本通知
    type = models.IntegerField(null=True, verbose_name=u'步骤类型')
    ord = models.IntegerField(null=True, verbose_name=u'小步骤执行的次序')
    # 块次序，从1开始
    blockOrd = models.IntegerField(null=True, verbose_name=u'块次序')
    blockName = models.CharField(max_length=255, null=True, verbose_name=u'块名称')
    account = models.CharField(max_length=255, null=True, verbose_name=u'目标机器的执行账户名')
    # # 目标机器的ip列表，逗号分割
    # ipListId = models.ForeignKey(Nm_ipList, verbose_name=u'目标机器的ip')
    # Agent异常的ip列表，逗号分割
    badIpList = models.CharField(max_length=255, null=True, verbose_name=u'Agent异常的ip列表')
    scriptContent = models.TextField(null=True, verbose_name=u'执行脚本的内容')
    # 执行脚本的类型:1(shell脚本)、2(bat脚本)、3(perl脚本)、4(python脚本)
    scriptType = models.IntegerField(null=True, verbose_name=u'执行脚本的类型')
    scriptParam = models.CharField(max_length=255, null=True, verbose_name=u'执行脚本的参数')
    scriptTimeout = models.IntegerField(null=True, verbose_name=u'执行脚本的超时时间')
    # 文件传输的源文件。格式：[{"file":"/home/data/backup/2.war","serverSetId":"1002",account:"root"},
    # {"file":"/home/data/a.txt","serverSetId":"1002",account:"root"}]如果是本地文件，那么只填file，
    # serverSetId，accont为空
    fileSource = models.TextField(null=True, verbose_name=u'文件传输的源文件')
    # 文件传输的目标目录，如：/home/data/backup
    fileTargetPath = models.CharField(max_length=255, null=True, verbose_name=u'文件传输的目标目录')
    # 传输文件的限速，单位KBps
    fileSpeedLimit = models.IntegerField(null=True, verbose_name=u'传输文件的限速')
    text = models.CharField(max_length=255, null=True, verbose_name=u'文本通知')
    operator = models.CharField(max_length=255, null=True, verbose_name=u'执行人')
    # 状态：1.未执行、2.正在执行、3.执行成功、4.执行失败、5.跳过、6.忽略错误、7.等待用户、
    #      8.手动结束、9.状态异常、10.步骤强制终止中、11.步骤强制终止成功、12.步骤强制终止失败
    status = models.IntegerField(null=True, default=1, verbose_name=u'状态')
    retryCount = models.IntegerField(null=True, default=1, verbose_name=u'重试次数')
    startTime = models.DateTimeField(null=True, verbose_name=u'开始时间')
    endTime = models.DateTimeField(null=True, verbose_name=u'结束时间')
    # 总耗时，单位：秒
    totalTime = models.FloatField(max_length=11, null=True, default=False, verbose_name=u'总耗时')
    totalIPNum = models.IntegerField(null=True, verbose_name=u'总ip数量')
    badIPNum = models.IntegerField(null=True, verbose_name=u'没有agent')
    runIPNum = models.IntegerField(null=True, verbose_name=u'有agent')
    failIPNum = models.IntegerField(null=True, verbose_name=u'失败ip数量')
    successIPNum = models.IntegerField(null=True, verbose_name=u'成功ip数量')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    # 是否需要暂停，1.需要暂停、0.不需要暂停，默认：0。
    isPause = models.IntegerField(null=True, default=0, verbose_name=u'是否需要暂停')
    companyId = models.IntegerField(null=True, default=0, verbose_name=u'开发商id')
    # 1.是  0.否
    isUseCCFileParam = models.IntegerField(null=True, default=0, verbose_name=u'')

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.status, self.totalTime)

    class Meta:
        db_table = 'nm_stepInstance'


class Nm_StepInstanceIpList(models.Model):
    """
    保存作业实例步骤目标服务器的执行结果
    """

    # 执行作业id: -1 快速执行脚本
    stepInstance = models.ForeignKey(Nm_StepInstance, null=True, verbose_name=u'执行作业实例步骤id')
    ip = models.CharField(max_length=255, null=True, verbose_name=u'ip地址')
    result = models.TextField(null=True, verbose_name=u'执行结果')

    def __unicode__(self):
        return '%s' % self.ip

    class Meta:
        db_table = 'nm_stepInstanceipList'


class Nm_Task(models.Model):
    # 作业

    appId = models.IntegerField(null=True, verbose_name=u'业务ID')
    name = models.CharField(max_length=255, null=True, unique=True, verbose_name=u'作业名称')
    account = models.CharField(max_length=255, null=True, verbose_name=u'目标机器的执行账户名')
    serverSetId = models.IntegerField(null=True, verbose_name=u'目标机器的服务器集合ID')
    # # 快速执行脚本时，执行作业名称=脚本名称 + 时间
    ipList = models.CharField(max_length=255, null=True, verbose_name=u'目标机器的IP,逗号分割')
    creater = models.CharField(max_length=255, null=True, verbose_name=u'执行人')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    lastModifyUser = models.CharField(max_length=255, null=True, verbose_name=u'最后修改人')
    lastModifyTime = models.DateTimeField(null=True, verbose_name=u'最后修改时间')
    tagId = models.IntegerField(null=True, verbose_name=u'标签Id')

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.creater, self.lastModifyTime)

    class Meta:
        db_table = 'nm_task'


class Nm_Step(models.Model):
    """
    作业步骤
    块名称blockName相当于步骤名称，每一个步骤里又分许多小步骤，小步骤名称对应的是name
    blockOrd 大步骤的执行顺序，ord小步骤的执行顺序
    """
    taskId = models.ForeignKey(Nm_Task, related_name="nm_task_set")
    appId = models.IntegerField(null=True, verbose_name=u'业务id')
    # 快速执行脚本时，执行步骤名称=脚本名称 + 时间
    name = models.CharField(max_length=255, null=True, verbose_name=u'节点名称')
    # 步骤类型：1、执行脚本，2、传输文件，3、文本通知
    type = models.IntegerField(null=True, verbose_name=u'步骤类型')
    ord = models.IntegerField(null=True, verbose_name=u'小步骤执行的次序')
    # 块次序，从1开始,大步骤执行顺序
    blockOrd = models.IntegerField(null=True, verbose_name=u'块次序')
    blockName = models.CharField(max_length=255, null=True, verbose_name=u'块名称')
    account = models.CharField(max_length=255, null=True, verbose_name=u'目标机器的执行账户名')
    # # 目标机器的ip列表，逗号分割
    serverSetId = models.CharField(max_length=255, null=True, verbose_name=u'服务器分组Id')
    # 目标机器的服务器IP，逗号分割，如果为空那么沿用作业的服务器IP
    ipList = models.CharField(max_length=255, null=True, verbose_name=u'目标机器的服务器IP')
    script = models.ForeignKey(Nm_Script, null=True, related_name='nm_script_set')
    scriptParam = models.CharField(max_length=255, null=True, verbose_name=u'执行脚本的参数')
    scriptTimeout = models.IntegerField(null=True, verbose_name=u'执行脚本的超时时间')
    # 文件传输的源文件。格式：[{"file":"/home/data/backup/2.war","serverSetId":"1002",account:"root"},
    # {"file":"/home/data/a.txt","serverSetId":"1002",account:"root"}]如果是本地文件，那么只填file，
    # serverSetId，accont为空
    fileSource = models.TextField(null=True, verbose_name=u'文件传输的源文件')
    # 文件传输的目标目录，如：/home/data/backup
    fileTargetPath = models.CharField(max_length=255, null=True, verbose_name=u'文件传输的目标目录')
    # 传输文件的限速，单位KBps
    fileSpeedLimit = models.IntegerField(null=True, verbose_name=u'传输文件的限速')
    text = models.CharField(max_length=255, null=True, verbose_name=u'文本通知')
    creater = models.CharField(max_length=255, null=True, verbose_name=u'创建人')
    createTime = models.DateTimeField(null=True, auto_now_add=True, verbose_name=u'创建时间')
    lastModifyUser = models.CharField(max_length=255, null=True, verbose_name=u'最后修改人')
    lastModifyTime = models.DateTimeField(null=True, verbose_name=u'最后修改时间')
    isPause = models.IntegerField(null=True, default=0, verbose_name=u'是否需要暂停')
    companyId = models.IntegerField(null=True, default=0, verbose_name=u'开发商id')
    ccScriptId = models.IntegerField(null=True, verbose_name=u'CC脚本ID')
    # 执行脚本入口参数类型 1.字符串入口参数  2.CC数据文件传参
    paramType = models.IntegerField(null=True, verbose_name=u'执行脚本入口参数类型')
    ccScriptParam = models.CharField(max_length=255, null=True, verbose_name=u'CC脚本的执行参数')
    ccServerSetId = models.IntegerField(null=True, verbose_name=u'cc服务器分组Id')
    useIpGlobleVar = models.IntegerField(null=True, verbose_name=u'IP服务器是否使用全局变量')

    def __unicode__(self):
        return '%s - %s - %s' % (self.taskId, self.name, self.type)

    class Meta:
        db_table = 'nm_step'


class Nm_StepIplist(models.Model):
    """
    作业步骤目标服务器的执行结果
    """
    step = models.ForeignKey(Nm_Step, null=True, verbose_name=u'作业步骤id')
    ip = models.CharField(max_length=255, null=True, verbose_name=u'ip地址')
    result = models.TextField(null=True, verbose_name=u'执行结果')

    def __unicode__(self):
        return '%s - %s' % (self.step, self.ip)

    class Meta:
        db_table = 'nm_stepipList'
