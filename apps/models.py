from django.db import models


# Create your models here.
class boxDeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0, verbose_name="箱号", blank=True, null=True)
    totalChnNum = models.IntegerField(default=0, verbose_name="总通道数", blank=True, null=True)


class wdjDeviceTable(models.Model):
    #一个对象映射实际中多个巡检仪，只需将其地址连续编址
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=1, verbose_name="485地址", blank=True, null=True)
    totalChnNum = models.IntegerField(default=20, verbose_name="总通道数", blank=True, null=True)
    protocolVersion = models.CharField(default='7',max_length=2,verbose_name="宇电表头协议版本号", blank=True, null=True)


class voltDeviceTable(models.Model):
    # 一个对象映射实际中多个巡检仪，只需将其地址连续编址
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=1, verbose_name="485地址", blank=True, null=True)
    totalChnNum = models.IntegerField(default=20, verbose_name="总通道数", blank=True, null=True)
    protocolVersion = models.CharField(default='7', max_length=2,verbose_name="宇电表头协议版本号", blank=True, null=True)


class H2DeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class N2DeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class H2ODeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class CO2DeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class CH4DeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class AIRDeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState =  models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="当前设定流量")
    nextState = models.DecimalField(max_digits=8, decimal_places=2,default=0, verbose_name="下一步设定流量")
    fullScale = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="满量程值")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=20001, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=0x20, verbose_name="485地址", blank=True, null=True)


class ovenPlanTable(models.Model):
    name = models.CharField(max_length=40, verbose_name="方案名", default="name", blank=True, null=True)
    date = models.DateTimeField(auto_now=True, verbose_name="方案创建时间", blank=True, null=True)
    steps = models.IntegerField(default=0, verbose_name="总步数")
    user = models.CharField(max_length=40, verbose_name="创建者", default="user", blank=True, null=True)

    def __str__(self):
        return 'Name:' + self.name


class ovenPlanDetailTable(models.Model):
    ovenPlanID = models.ForeignKey(ovenPlanTable, to_field='id', verbose_name="炉子测试方案ID", on_delete=models.CASCADE)
    step = models.IntegerField(default=1, verbose_name="工步号")
    T = models.IntegerField(default=0, verbose_name="目标温度")
    time = models.IntegerField(default=0, verbose_name="工步持续时间")


class ovenDeviceTable(models.Model):
    ID = models.CharField(max_length=8, verbose_name="设备编号", primary_key=True, unique=True)
    currState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="当前状态", default="stop")
    nextState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="下一步状态", default="stop")
    IP = models.GenericIPAddressField(default='192.168.0.3', verbose_name="IP地址", blank=True, null=True)
    PortNum = models.IntegerField(default=0, verbose_name="端口号", blank=True, null=True)
    Addr = models.IntegerField(default=1, verbose_name="485地址", blank=True, null=True)
    ovenPlanID = models.ForeignKey(ovenPlanTable, to_field='id', verbose_name="炉子测试方案ID", on_delete=models.CASCADE,
                                   null=True, blank=True)
    protocolVersion = models.CharField(default='7', max_length=2,verbose_name="宇电表头协议版本号", blank=True, null=True)


class cellDeviceTable(models.Model):
    cellID = models.CharField(max_length=8, verbose_name="电池/电堆编号", primary_key=True, unique=True)
    # 电子负载信息
    boxID = models.ForeignKey(boxDeviceTable, to_field='ID', verbose_name="负载ID", on_delete=models.CASCADE, blank=True,
                              null=True)
    chnNum = models.IntegerField(default=0, verbose_name="通道号", blank=True, null=True)

    # H2流量计
    mH2ID = models.ForeignKey(H2DeviceTable, to_field='ID', verbose_name="H2流量计ID", on_delete=models.CASCADE,
                              blank=True, null=True)
    coefH2 = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # N2流量计
    mN2ID = models.ForeignKey(N2DeviceTable, to_field='ID', verbose_name="N2流量计ID", on_delete=models.CASCADE,
                              blank=True, null=True)
    coefN2 = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # CH4流量计
    mCH4ID = models.ForeignKey(CH4DeviceTable, to_field='ID', verbose_name="CH4流量计ID",
                               on_delete=models.CASCADE, blank=True, null=True)
    coefCH4 = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # H2O流量计
    mH2OID = models.ForeignKey(H2ODeviceTable, to_field='ID', verbose_name="H2O流量计ID",
                               on_delete=models.CASCADE, blank=True, null=True)
    coefH2O = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # AIR流量计
    mAIRID = models.ForeignKey(AIRDeviceTable, to_field='ID', verbose_name="AIR流量计ID",
                               on_delete=models.CASCADE, blank=True, null=True)
    coefAIR = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # CO2流量计
    mCO2ID = models.ForeignKey(CO2DeviceTable, to_field='ID', verbose_name="CO2流量计ID",
                               on_delete=models.CASCADE, blank=True, null=True)
    coefCO2 = models.DecimalField(max_digits=2, decimal_places=1, default=0, verbose_name="比率系数", blank=True, null=True)

    # Tc控温点
    mTc0ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="温控器ID", on_delete=models.CASCADE,
                               blank=True,null=True,related_name='first_oven')
    mTc1ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="温控器ID", on_delete=models.CASCADE,
                               blank=True,null=True,related_name='second_oven')
    mTc2ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="温控器ID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='third_oven')
    mTc3ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="温控器ID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='fourth_oven')

    # Tm测温点
    mTmID = models.ForeignKey(wdjDeviceTable, to_field='ID', verbose_name="温度计ID", on_delete=models.CASCADE,
                               blank=True, null=True)

    # Vm电压表
    mVmID = models.ForeignKey(voltDeviceTable, to_field='ID', verbose_name="电压表ID", on_delete=models.CASCADE,
                               blank=True, null=True)



    def __str__(self):
        return "CellID:" + str(self.cellID) + '  BoxID:' + str(self.boxID) + '  ChannelID:' + str(self.chnNum)


class cellPlanTable(models.Model):
    name = models.CharField(max_length=40, verbose_name="方案名", default="name", blank=True, null=True)
    date = models.DateTimeField(auto_now=True, verbose_name="方案创建时间", blank=True, null=True)
    steps = models.IntegerField(default=0, verbose_name="总工步数")
    user = models.CharField(max_length=40, verbose_name="创建者", default="user", blank=True, null=True)

    def __str__(self):
        return str(self.id) + ":" + self.name


class cellPlanDetailTable(models.Model):
    planID = models.ForeignKey(cellPlanTable, to_field='id', verbose_name="电子负载测试方案ID", on_delete=models.CASCADE)
    step = models.IntegerField(default=1, verbose_name="工步号")
    # 电子负载控制
    mode = models.CharField(choices=(
        ("停止", "停止"), ("静置", "静置"), ("恒流充电", "恒流充电"), ("恒流放电", "恒流放电"), ("恒压充电", "恒压充电"), ("恒压放电", "恒压放电"),
        ("恒压限流充电", "恒压限流充电"), ("恒压限流放电", "恒压限流放电"), ("恒阻放电", "恒阻放电"), ("恒功率充电", "恒功率充电"), ("恒功率放电", "恒功率放电"),
        ("循环", "循环"), ("跳转", "跳转"), ("电压采样", "电压采样")),
        max_length=10, verbose_name="工作模式", default="静置")
    # 电子负载工步参数
    i = models.IntegerField(verbose_name="电流/uA", blank=True, null=True)
    u = models.IntegerField(verbose_name="电压/uV", blank=True, null=True)
    r = models.IntegerField(verbose_name="电阻/ohm", blank=True, null=True)
    p = models.IntegerField(verbose_name="功率/W", blank=True, null=True)
    n = models.IntegerField(verbose_name="循环次数", blank=True, null=True)
    nStart = models.IntegerField(verbose_name="循环开始工步", blank=True, null=True)
    nStop = models.IntegerField(verbose_name="循环结束工步", blank=True, null=True)
    nTarget = models.IntegerField(verbose_name="跳转工步号", blank=True, null=True)
    # 电子负载限制条件
    tTH = models.IntegerField(verbose_name="时间限制/ms", blank=True, null=True)  # s
    iTH = models.IntegerField(verbose_name="电流限制/uA", blank=True, null=True)  # uA
    uTH = models.IntegerField(verbose_name="电压限制/uV", blank=True, null=True)  # uV
    qTH = models.IntegerField(verbose_name="容量限制/uAh", blank=True, null=True)  #
    qATH = models.IntegerField(verbose_name="累计容量限制/uAh", blank=True, null=True)  # s
    # 工步记录条件
    recordMode = models.CharField(
        choices=(("无", "无"), ("定时差", "定时差"), ("定压差", "定压差"), ("定流差", "定流差"), ("定容差", "定容差"), ("固定电压尾数", "固定电压尾数")),
        max_length=10, verbose_name="工步记录条件", default="无", blank=True, null=True)
    recordPara = models.IntegerField(verbose_name="工步记录参数", blank=True, null=True)
    # 整体记录条件
    tRECORD = models.IntegerField(verbose_name="定时差记录/ms", blank=True, null=True)
    uRECORD = models.IntegerField(verbose_name="定压差记录/uV", blank=True, null=True)
    iRECORD = models.IntegerField(verbose_name="定流差记录/uA", blank=True, null=True)
    qRECORD = models.IntegerField(verbose_name="定容差记录/uAh", blank=True, null=True)
    # 电子负载保护条件
    imaxProtect = models.IntegerField(verbose_name="过流保护", blank=True, null=True)
    iminProtect = models.IntegerField(verbose_name="欠流保护", blank=True, null=True)
    umaxProtect = models.IntegerField(verbose_name="过压保护", blank=True, null=True)
    uminProtect = models.IntegerField(verbose_name="欠压保护", blank=True, null=True)
    TmaxProtect = models.IntegerField(verbose_name="高温保护", blank=True, null=True)
    TminProtect = models.IntegerField(verbose_name="低温保护", blank=True, null=True)

    def __str__(self):
        return "PlanID:" + str(self.planID) + '  Step:' + str(self.step)


class BigTestInfoTable(models.Model):
    name = models.CharField(max_length=40, verbose_name="测试名", default="name", blank=True, null=True)
    user = models.CharField(max_length=40, verbose_name="创建者", default="user", blank=True, null=True)
    cellID = models.ForeignKey(cellDeviceTable, to_field='cellID', verbose_name="cellID", on_delete=models.CASCADE,
                               null=True, blank=True)
    boxID = models.ForeignKey(boxDeviceTable, to_field='ID', verbose_name="boxID", on_delete=models.CASCADE, null=True,
                              blank=True)
    chnNum = models.IntegerField(default=0, verbose_name="通道号", null=True, blank=True)
    H2ID = models.ForeignKey(H2DeviceTable, to_field='ID', verbose_name="H2ID", on_delete=models.CASCADE, blank=True,
                             null=True)
    N2ID = models.ForeignKey(N2DeviceTable, to_field='ID', verbose_name="N2ID", on_delete=models.CASCADE, blank=True,
                             null=True)
    H2OID = models.ForeignKey(H2ODeviceTable, to_field='ID', verbose_name="H2OID", on_delete=models.CASCADE, blank=True,
                              null=True)
    CH4ID = models.ForeignKey(CH4DeviceTable, to_field='ID', verbose_name="CH4ID", on_delete=models.CASCADE, blank=True,
                              null=True)
    CO2ID = models.ForeignKey(CO2DeviceTable, to_field='ID', verbose_name="CO2ID", on_delete=models.CASCADE, blank=True,
                              null=True)
    AIRID = models.ForeignKey(AIRDeviceTable, to_field='ID', verbose_name="AIRID", on_delete=models.CASCADE, blank=True,
                              null=True)
    wdjID = models.ForeignKey(wdjDeviceTable, to_field='ID', verbose_name="wdj0ID", on_delete=models.CASCADE, blank=True,
                              null=True)
    voltID = models.ForeignKey(voltDeviceTable, to_field='ID', verbose_name="volt0ID", on_delete=models.CASCADE,
                               blank=True,null=True)
    oven0ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="ovenID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='firstoven')
    oven1ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="ovenID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='secondoven')
    oven2ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="ovenID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='thirdoven')
    oven3ID = models.ForeignKey(ovenDeviceTable, to_field='ID', verbose_name="ovenID", on_delete=models.CASCADE,
                               blank=True, null=True,related_name='fourthoven')
    startDate = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    endDate = models.DateTimeField(verbose_name="结束时间", blank=True, null=True)
    completeFlag = models.IntegerField(default=0, verbose_name="完成标志")


class testInfoTable(models.Model):
    name = models.CharField(max_length=40, verbose_name="测试名", default="name", blank=True, null=True)
    user = models.CharField(max_length=40, verbose_name="创建者", default="user", blank=True, null=True)
    cellID = models.ForeignKey(cellDeviceTable, to_field='cellID', verbose_name="cellID", on_delete=models.CASCADE)
    boxID = models.ForeignKey(boxDeviceTable, to_field='ID', verbose_name="boxID", on_delete=models.CASCADE)
    chnNum = models.IntegerField(default=0, verbose_name="通道号")
    bigTestID = models.ForeignKey(BigTestInfoTable, to_field='id', verbose_name="大测试ID", on_delete=models.CASCADE)
    planID = models.ForeignKey(cellPlanTable, to_field='id', verbose_name="测试方案ID", on_delete=models.CASCADE,
                               blank=True, null=True)
    startDate = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    endDate = models.DateTimeField(verbose_name="结束时间", blank=True, null=True)
    completeFlag = models.IntegerField(default=0, verbose_name="完成标志")


class cellTestRealDataTable(models.Model):
    # 电池ID
    cellID = models.ForeignKey(cellDeviceTable, to_field='cellID', verbose_name="cellID", on_delete=models.CASCADE,
                               null=True, blank=True)
    boxID = models.ForeignKey(boxDeviceTable, to_field='ID', verbose_name="箱号", on_delete=models.CASCADE, null=True,
                              blank=True)
    chnNum = models.IntegerField(default=0, verbose_name="通道号", null=True, blank=True)
    # 测试ID，区别于测试方案ID
    bigTestID = models.ForeignKey(BigTestInfoTable, to_field='id', verbose_name="bigTestID", on_delete=models.CASCADE)
    testID = models.ForeignKey(testInfoTable, to_field='id', verbose_name="testID", on_delete=models.CASCADE,
                               blank=True, null=True)
    # 测试方案信息
    totalStepN = models.IntegerField(default=0, verbose_name="总工步数", blank=True, null=True)
    currState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="当前状态", default="stop", null=True, blank=True)
    nextState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="下一步状态", default="stop", null=True, blank=True)

    # 电池运行状态信息
    conState = models.IntegerField(default=0, verbose_name="联机状态", blank=True, null=True)
    chState = models.IntegerField(default=0, verbose_name="通道状态", blank=True, null=True)
    chStateCode = models.IntegerField(default=0, verbose_name="通道异常代码", blank=True, null=True)

    chMasterSlaveFlag = models.IntegerField(default=0, verbose_name="通道主从标志", blank=True, null=True)
    n = models.IntegerField(default=0, verbose_name="当前工步号", blank=True, null=True)  #
    k = models.IntegerField(default=0, verbose_name="当前过程号", blank=True, null=True)  #
    mode = models.IntegerField(default=0, verbose_name="工作模式", blank=True, null=True)  #

    tc = models.IntegerField(default=0, verbose_name="本工步已工作时间", blank=True, null=True)  # ms
    ta = models.IntegerField(default=0, verbose_name="本工步累计时间", blank=True, null=True)

    i = models.IntegerField(default=0, verbose_name="实时电流", blank=True, null=True)  # uA
    u = models.IntegerField(default=0, verbose_name="实时电压", blank=True, null=True)  # mV
    q = models.IntegerField(default=0, verbose_name="实时容量", blank=True, null=True)  #
    qA = models.IntegerField(default=0, verbose_name="累计容量", blank=True, null=True)  #
    T = models.IntegerField(default=0, verbose_name="当前温度", blank=True, null=True)  #
    r = models.IntegerField(default=0, verbose_name="当前内阻", blank=True, null=True)  #

    detailDataFlag = models.IntegerField(default=0, verbose_name="是否有明细数据", blank=True, null=True)
    resultDataFlag = models.IntegerField(default=0, verbose_name="是否有结果数据", blank=True, null=True)
    overOutDataFlag = models.IntegerField(default=0, verbose_name="是否有数据溢出", blank=True, null=True)
    powerDownFlag = models.IntegerField(default=0, verbose_name="是否有设备断电", blank=True, null=True)

    celldata_time = models.DateTimeField(auto_now=True, verbose_name="电池数据修改时间", blank=True, null=True)

    # 流量计信息
    sH2 = models.IntegerField(default=0, verbose_name="H2通讯状态", blank=True, null=True)
    qH2 = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="H2流量", blank=True, null=True)
    tH2 = models.DateTimeField(auto_now=True, verbose_name="H2数据修改时间", blank=True, null=True)

    sN2 = models.IntegerField(default=0, verbose_name="N2通讯状态", blank=True, null=True)
    qN2 = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="N2流量", blank=True, null=True)
    tN2 = models.DateTimeField(auto_now=True, verbose_name="N2数据修改时间", blank=True, null=True)

    sCO2 = models.IntegerField(default=0, verbose_name="CO2通讯状态", blank=True, null=True)
    qCO2 = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="CO2流量", blank=True, null=True)
    tCO2 = models.DateTimeField(auto_now=True, verbose_name="CO2数据修改时间", blank=True, null=True)

    sCH4 = models.IntegerField(default=0, verbose_name="CH4通讯状态", blank=True, null=True)
    qCH4 = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="CH4流量", blank=True, null=True)
    tCH4 = models.DateTimeField(auto_now=True, verbose_name="CH4数据修改时间", blank=True, null=True)

    sAIR = models.IntegerField(default=0, verbose_name="AIR通讯状态", blank=True, null=True)
    qAIR = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="空气流量", blank=True, null=True)
    tAIR = models.DateTimeField(auto_now=True, verbose_name="AIR数据修改时间", blank=True, null=True)

    sH2O = models.IntegerField(default=0, verbose_name="H2O通讯状态", blank=True, null=True)
    qH2O = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="水流量", blank=True, null=True)
    tH2O = models.DateTimeField(auto_now=True, verbose_name="H2O数据修改时间", blank=True, null=True)

    # 温控器信息
    sTc0 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点0", blank=True, null=True)
    tTc0 = models.DateTimeField(auto_now=True, verbose_name="T0数据修改时间", blank=True, null=True)

    sTc1 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点1", blank=True, null=True)
    tTc1 = models.DateTimeField(auto_now=True, verbose_name="T1数据修改时间", blank=True, null=True)

    sTc2 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点2", blank=True, null=True)
    tTc2 = models.DateTimeField(auto_now=True, verbose_name="T2数据修改时间", blank=True, null=True)

    sTc3 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点3", blank=True, null=True)
    tTc3 = models.DateTimeField(auto_now=True, verbose_name="T3数据修改时间", blank=True, null=True)

    #温度巡检仪信息
    Tm0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点0", blank=True, null=True)
    tTm0 = models.DateTimeField(auto_now=True, verbose_name="T0数据修改时间", blank=True, null=True)
    Tm1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点1", blank=True, null=True)
    tTm1 = models.DateTimeField(auto_now=True, verbose_name="T1数据修改时间", blank=True, null=True)
    Tm2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点2", blank=True, null=True)
    tTm2 = models.DateTimeField(auto_now=True, verbose_name="T2数据修改时间", blank=True, null=True)
    Tm3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点3", blank=True, null=True)
    tTm3 = models.DateTimeField(auto_now=True, verbose_name="T3数据修改时间", blank=True, null=True)
    Tm4 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点4", blank=True, null=True)
    tTm4 = models.DateTimeField(auto_now=True, verbose_name="T4数据修改时间", blank=True, null=True)
    Tm5 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点5", blank=True, null=True)
    tTm5 = models.DateTimeField(auto_now=True, verbose_name="T5数据修改时间", blank=True, null=True)
    Tm6 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点6", blank=True, null=True)
    tTm6 = models.DateTimeField(auto_now=True, verbose_name="T6数据修改时间", blank=True, null=True)
    Tm7 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点7", blank=True, null=True)
    tTm7 = models.DateTimeField(auto_now=True, verbose_name="T7数据修改时间", blank=True, null=True)
    Tm8 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点8", blank=True, null=True)
    tTm8 = models.DateTimeField(auto_now=True, verbose_name="T8数据修改时间", blank=True, null=True)
    Tm9 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点9", blank=True, null=True)
    tTm9 = models.DateTimeField(auto_now=True, verbose_name="T9数据修改时间", blank=True, null=True)
    Tm10 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点10", blank=True, null=True)
    tTm10 = models.DateTimeField(auto_now=True, verbose_name="T10数据修改时间", blank=True, null=True)
    Tm11 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点11", blank=True, null=True)
    tTm11 = models.DateTimeField(auto_now=True, verbose_name="T11数据修改时间", blank=True, null=True)
    Tm12 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点12", blank=True, null=True)
    tTm12 = models.DateTimeField(auto_now=True, verbose_name="T12数据修改时间", blank=True, null=True)
    Tm13 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点13", blank=True, null=True)
    tTm13 = models.DateTimeField(auto_now=True, verbose_name="T13数据修改时间", blank=True, null=True)
    Tm14 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点14", blank=True, null=True)
    tTm14 = models.DateTimeField(auto_now=True, verbose_name="T14数据修改时间", blank=True, null=True)
    Tm15 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点15", blank=True, null=True)
    tTm15 = models.DateTimeField(auto_now=True, verbose_name="T15数据修改时间", blank=True, null=True)
    Tm16 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点16", blank=True, null=True)
    tTm16 = models.DateTimeField(auto_now=True, verbose_name="T16数据修改时间", blank=True, null=True)
    Tm17 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点17", blank=True, null=True)
    tTm17 = models.DateTimeField(auto_now=True, verbose_name="T17数据修改时间", blank=True, null=True)
    Tm18 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点18", blank=True, null=True)
    tTm18 = models.DateTimeField(auto_now=True, verbose_name="T18数据修改时间", blank=True, null=True)
    Tm19 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点19", blank=True, null=True)
    tTm19 = models.DateTimeField(auto_now=True, verbose_name="T19数据修改时间", blank=True, null=True)

    # 电压巡检仪信息
    Vm0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点0", blank=True, null=True)
    tVm0 = models.DateTimeField(auto_now=True, verbose_name="V0数据修改时间", blank=True, null=True)
    Vm1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点1", blank=True, null=True)
    tVm1 = models.DateTimeField(auto_now=True, verbose_name="V1数据修改时间", blank=True, null=True)
    Vm2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点2", blank=True, null=True)
    tVm2 = models.DateTimeField(auto_now=True, verbose_name="V2数据修改时间", blank=True, null=True)
    Vm3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点3", blank=True, null=True)
    tVm3 = models.DateTimeField(auto_now=True, verbose_name="V3数据修改时间", blank=True, null=True)
    Vm4 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点4", blank=True, null=True)
    tVm4 = models.DateTimeField(auto_now=True, verbose_name="V4数据修改时间", blank=True, null=True)
    Vm5 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点5", blank=True, null=True)
    tVm5 = models.DateTimeField(auto_now=True, verbose_name="V5数据修改时间", blank=True, null=True)
    Vm6 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点6", blank=True, null=True)
    tVm6 = models.DateTimeField(auto_now=True, verbose_name="V6数据修改时间", blank=True, null=True)
    Vm7 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点7", blank=True, null=True)
    tVm7 = models.DateTimeField(auto_now=True, verbose_name="V7数据修改时间", blank=True, null=True)
    Vm8 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点8", blank=True, null=True)
    tVm8 = models.DateTimeField(auto_now=True, verbose_name="V8数据修改时间", blank=True, null=True)
    Vm9 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点9", blank=True, null=True)
    tVm9 = models.DateTimeField(auto_now=True, verbose_name="V9数据修改时间", blank=True, null=True)
    Vm10 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点10", blank=True, null=True)
    tVm10 = models.DateTimeField(auto_now=True, verbose_name="V10数据修改时间", blank=True, null=True)
    Vm11 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点11", blank=True, null=True)
    tVm11 = models.DateTimeField(auto_now=True, verbose_name="V11数据修改时间", blank=True, null=True)
    Vm12 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点12", blank=True, null=True)
    tVm12 = models.DateTimeField(auto_now=True, verbose_name="V12数据修改时间", blank=True, null=True)
    Vm13 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点13", blank=True, null=True)
    tVm13 = models.DateTimeField(auto_now=True, verbose_name="V13数据修改时间", blank=True, null=True)
    Vm14 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点14", blank=True, null=True)
    tVm14 = models.DateTimeField(auto_now=True, verbose_name="V14数据修改时间", blank=True, null=True)
    Vm15 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点15", blank=True, null=True)
    tVm15 = models.DateTimeField(auto_now=True, verbose_name="V15数据修改时间", blank=True, null=True)
    Vm16 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点16", blank=True, null=True)
    tVm16 = models.DateTimeField(auto_now=True, verbose_name="V16数据修改时间", blank=True, null=True)
    Vm17 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点17", blank=True, null=True)
    tVm17 = models.DateTimeField(auto_now=True, verbose_name="V17数据修改时间", blank=True, null=True)
    Vm18 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点18", blank=True, null=True)
    tVm18 = models.DateTimeField(auto_now=True, verbose_name="V18数据修改时间", blank=True, null=True)
    Vm19 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点19", blank=True, null=True)
    tVm19 = models.DateTimeField(auto_now=True, verbose_name="V19数据修改时间", blank=True, null=True)

    def __str__(self):
        return str(self.testID)


class eventTable(models.Model):
    date = models.DateTimeField(auto_now=True, verbose_name="T4数据修改时间")
    cellID = models.ForeignKey(cellDeviceTable, to_field='cellID', verbose_name="cellID", on_delete=models.DO_NOTHING,
                               null=True, blank=True)
    boxID = models.IntegerField(default=0, verbose_name="箱号", null=True, blank=True)  #
    chnNum = models.IntegerField(default=0, verbose_name="通道号", null=True, blank=True)
    testID = models.ForeignKey(testInfoTable, to_field='id', verbose_name="测试ID", on_delete=models.CASCADE)
    planID = models.ForeignKey(cellPlanTable, to_field='id', verbose_name="测试方案ID", on_delete=models.CASCADE)
    stepNum = models.IntegerField(default=0, verbose_name="工步号", blank=True)
    objectType = models.CharField(choices=(
        ("H2", "恒流"), ("N2", "恒压"), ("CH4", "静置"), ("H2O", "循环"), ("AIR", "循环"), ("RES", "循环"), ("T1", "循环"),
        ("T2", "循环"),
        ("T3", "循环"), ("T4", "循环"), ("eLoad", "电子负载")), max_length=10, verbose_name="告警对象", default="eLoad", blank=True)
    content = models.TextField(max_length=8, verbose_name="事件内容")


class cellTestHistoryDataTable(models.Model):
    bigTestID = models.ForeignKey(BigTestInfoTable, to_field='id', verbose_name="bigTestID", on_delete=models.CASCADE)
    testID = models.ForeignKey(testInfoTable, to_field='id', verbose_name="testID", on_delete=models.CASCADE,
                               blank=True, null=True)
    # 测试方案信息
    totalStepN = models.IntegerField(default=0, verbose_name="总工步数", blank=True, null=True)
    currState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="当前状态", blank=True, null=True)
    nextState = models.CharField(choices=(("stop", "停止"), ("pause", "暂停"), ("start", "启动"), ("resume", "继续")),
                                 max_length=10, verbose_name="下一步状态", blank=True, null=True)

    # 电池运行状态信息
    conState = models.IntegerField(default=0, verbose_name="联机状态", null=True, blank=True)
    chState = models.IntegerField(default=0, verbose_name="通道状态", null=True, blank=True)
    chStateCode = models.IntegerField(default=0, verbose_name="通道异常代码", null=True, blank=True)

    chMasterSlaveFlag = models.IntegerField(default=0, verbose_name="通道主从标志", null=True, blank=True)
    n = models.IntegerField(default=0, verbose_name="当前工步号", blank=True, null=True)  #
    k = models.IntegerField(default=0, verbose_name="当前过程号", blank=True, null=True)  #
    mode = models.IntegerField(default=0, verbose_name="工作模式", blank=True, null=True)  #

    tc = models.IntegerField(default=0, verbose_name="本工步已工作时间", blank=True, null=True)  # ms
    ta = models.IntegerField(default=0, verbose_name="本工步累计时间", blank=True, null=True)

    i = models.IntegerField(default=0, verbose_name="实时电流", blank=True, null=True)  # uA
    u = models.IntegerField(default=0, verbose_name="实时电压", blank=True, null=True)  # mV
    q = models.IntegerField(default=0, verbose_name="实时容量", blank=True, null=True)  #
    qA = models.IntegerField(default=0, verbose_name="累计容量", blank=True, null=True)  #
    T = models.IntegerField(default=0, verbose_name="当前温度", blank=True, null=True)  #
    r = models.IntegerField(default=0, verbose_name="当前内阻", blank=True, null=True)  #

    detailDataFlag = models.IntegerField(default=0, verbose_name="是否有明细数据", blank=True, null=True)
    resultDataFlag = models.IntegerField(default=0, verbose_name="是否有结果数据", blank=True, null=True)
    overOutDataFlag = models.IntegerField(default=0, verbose_name="是否有数据溢出", blank=True, null=True)
    powerDownFlag = models.IntegerField(default=0, verbose_name="是否有设备断电", blank=True, null=True)

    celldata_time = models.DateTimeField(auto_now=True, verbose_name="电池数据修改时间", null=True, blank=True)

    # 流量计信息
    sH2 = models.IntegerField(default=0, verbose_name="H2通讯状态", null=True, blank=True)
    qH2 = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="H2流量", null=True, blank=True)
    tH2 = models.DateTimeField(auto_now=True, verbose_name="H2数据修改时间", null=True, blank=True)

    sN2 = models.IntegerField(default=0, verbose_name="N2通讯状态", null=True, blank=True)
    qN2 = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="N2流量", null=True, blank=True)
    tN2 = models.DateTimeField(auto_now=True, verbose_name="N2数据修改时间", null=True, blank=True)

    sCO2 = models.IntegerField(default=0, verbose_name="CO2通讯状态", null=True, blank=True)
    qCO2 = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="CO2流量", null=True, blank=True)
    tCO2 = models.DateTimeField(auto_now=True, verbose_name="CO2数据修改时间", null=True, blank=True)

    sCH4 = models.IntegerField(default=0, verbose_name="CH4通讯状态", null=True, blank=True)
    qCH4 = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="CH4流量", null=True, blank=True)
    tCH4 = models.DateTimeField(auto_now=True, verbose_name="CH4数据修改时间", null=True, blank=True)

    sAIR = models.IntegerField(default=0, verbose_name="AIR通讯状态", null=True, blank=True)
    qAIR = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="空气流量", null=True, blank=True)
    tAIR = models.DateTimeField(auto_now=True, verbose_name="AIR数据修改时间", null=True, blank=True)

    sH2O = models.IntegerField(default=0, verbose_name="H2O通讯状态", null=True, blank=True)
    qH2O = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="水流量", null=True, blank=True)
    tH2O = models.DateTimeField(auto_now=True, verbose_name="H2O数据修改时间", null=True, blank=True)

    # 温控器信息
    sTc0 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点0", blank=True, null=True)
    tTc0 = models.DateTimeField(auto_now=True, verbose_name="T0数据修改时间", blank=True, null=True)

    sTc1 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点1", blank=True, null=True)
    tTc1 = models.DateTimeField(auto_now=True, verbose_name="T1数据修改时间", blank=True, null=True)

    sTc2 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点2", blank=True, null=True)
    tTc2 = models.DateTimeField(auto_now=True, verbose_name="T2数据修改时间", blank=True, null=True)

    sTc3 = models.IntegerField(default=0, verbose_name="通讯状态", blank=True, null=True)
    Tc3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度控制点3", blank=True, null=True)
    tTc3 = models.DateTimeField(auto_now=True, verbose_name="T3数据修改时间", blank=True, null=True)

    #温度巡检仪信息
    Tm0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点0", blank=True, null=True)
    tTm0 = models.DateTimeField(auto_now=True, verbose_name="T0数据修改时间", blank=True, null=True)
    Tm1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点1", blank=True, null=True)
    tTm1 = models.DateTimeField(auto_now=True, verbose_name="T1数据修改时间", blank=True, null=True)
    Tm2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点2", blank=True, null=True)
    tTm2 = models.DateTimeField(auto_now=True, verbose_name="T2数据修改时间", blank=True, null=True)
    Tm3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点3", blank=True, null=True)
    tTm3 = models.DateTimeField(auto_now=True, verbose_name="T3数据修改时间", blank=True, null=True)
    Tm4 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点4", blank=True, null=True)
    tTm4 = models.DateTimeField(auto_now=True, verbose_name="T4数据修改时间", blank=True, null=True)
    Tm5 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点5", blank=True, null=True)
    tTm5 = models.DateTimeField(auto_now=True, verbose_name="T5数据修改时间", blank=True, null=True)
    Tm6 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点6", blank=True, null=True)
    tTm6 = models.DateTimeField(auto_now=True, verbose_name="T6数据修改时间", blank=True, null=True)
    Tm7 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点7", blank=True, null=True)
    tTm7 = models.DateTimeField(auto_now=True, verbose_name="T7数据修改时间", blank=True, null=True)
    Tm8 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点8", blank=True, null=True)
    tTm8 = models.DateTimeField(auto_now=True, verbose_name="T8数据修改时间", blank=True, null=True)
    Tm9 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点9", blank=True, null=True)
    tTm9 = models.DateTimeField(auto_now=True, verbose_name="T9数据修改时间", blank=True, null=True)
    Tm10 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点10", blank=True, null=True)
    tTm10 = models.DateTimeField(auto_now=True, verbose_name="T10数据修改时间", blank=True, null=True)
    Tm11 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点11", blank=True, null=True)
    tTm11 = models.DateTimeField(auto_now=True, verbose_name="T11数据修改时间", blank=True, null=True)
    Tm12 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点12", blank=True, null=True)
    tTm12 = models.DateTimeField(auto_now=True, verbose_name="T12数据修改时间", blank=True, null=True)
    Tm13 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点13", blank=True, null=True)
    tTm13 = models.DateTimeField(auto_now=True, verbose_name="T13数据修改时间", blank=True, null=True)
    Tm14 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点14", blank=True, null=True)
    tTm14 = models.DateTimeField(auto_now=True, verbose_name="T14数据修改时间", blank=True, null=True)
    Tm15 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点15", blank=True, null=True)
    tTm15 = models.DateTimeField(auto_now=True, verbose_name="T15数据修改时间", blank=True, null=True)
    Tm16 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点16", blank=True, null=True)
    tTm16 = models.DateTimeField(auto_now=True, verbose_name="T16数据修改时间", blank=True, null=True)
    Tm17 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点17", blank=True, null=True)
    tTm17 = models.DateTimeField(auto_now=True, verbose_name="T17数据修改时间", blank=True, null=True)
    Tm18 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点18", blank=True, null=True)
    tTm18 = models.DateTimeField(auto_now=True, verbose_name="T18数据修改时间", blank=True, null=True)
    Tm19 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="温度监测点19", blank=True, null=True)
    tTm19 = models.DateTimeField(auto_now=True, verbose_name="T19数据修改时间", blank=True, null=True)

    # 电压巡检仪信息
    Vm0 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点0", blank=True, null=True)
    tVm0 = models.DateTimeField(auto_now=True, verbose_name="V0数据修改时间", blank=True, null=True)
    Vm1 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点1", blank=True, null=True)
    tVm1 = models.DateTimeField(auto_now=True, verbose_name="V1数据修改时间", blank=True, null=True)
    Vm2 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点2", blank=True, null=True)
    tVm2 = models.DateTimeField(auto_now=True, verbose_name="V2数据修改时间", blank=True, null=True)
    Vm3 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点3", blank=True, null=True)
    tVm3 = models.DateTimeField(auto_now=True, verbose_name="V3数据修改时间", blank=True, null=True)
    Vm4 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点4", blank=True, null=True)
    tVm4 = models.DateTimeField(auto_now=True, verbose_name="V4数据修改时间", blank=True, null=True)
    Vm5 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点5", blank=True, null=True)
    tVm5 = models.DateTimeField(auto_now=True, verbose_name="V5数据修改时间", blank=True, null=True)
    Vm6 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点6", blank=True, null=True)
    tVm6 = models.DateTimeField(auto_now=True, verbose_name="V6数据修改时间", blank=True, null=True)
    Vm7 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点7", blank=True, null=True)
    tVm7 = models.DateTimeField(auto_now=True, verbose_name="V7数据修改时间", blank=True, null=True)
    Vm8 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点8", blank=True, null=True)
    tVm8 = models.DateTimeField(auto_now=True, verbose_name="V8数据修改时间", blank=True, null=True)
    Vm9 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点9", blank=True, null=True)
    tVm9 = models.DateTimeField(auto_now=True, verbose_name="V9数据修改时间", blank=True, null=True)
    Vm10 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点10", blank=True, null=True)
    tVm10 = models.DateTimeField(auto_now=True, verbose_name="V10数据修改时间", blank=True, null=True)
    Vm11 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点11", blank=True, null=True)
    tVm11 = models.DateTimeField(auto_now=True, verbose_name="V11数据修改时间", blank=True, null=True)
    Vm12 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点12", blank=True, null=True)
    tVm12 = models.DateTimeField(auto_now=True, verbose_name="V12数据修改时间", blank=True, null=True)
    Vm13 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点13", blank=True, null=True)
    tVm13 = models.DateTimeField(auto_now=True, verbose_name="V13数据修改时间", blank=True, null=True)
    Vm14 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点14", blank=True, null=True)
    tVm14 = models.DateTimeField(auto_now=True, verbose_name="V14数据修改时间", blank=True, null=True)
    Vm15 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点15", blank=True, null=True)
    tVm15 = models.DateTimeField(auto_now=True, verbose_name="V15数据修改时间", blank=True, null=True)
    Vm16 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点16", blank=True, null=True)
    tVm16 = models.DateTimeField(auto_now=True, verbose_name="V16数据修改时间", blank=True, null=True)
    Vm17 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点17", blank=True, null=True)
    tVm17 = models.DateTimeField(auto_now=True, verbose_name="V17数据修改时间", blank=True, null=True)
    Vm18 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点18", blank=True, null=True)
    tVm18 = models.DateTimeField(auto_now=True, verbose_name="V18数据修改时间", blank=True, null=True)
    Vm19 = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="电压监测点19", blank=True, null=True)
    tVm19 = models.DateTimeField(auto_now=True, verbose_name="V19数据修改时间", blank=True, null=True)
