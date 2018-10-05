#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from dbClass import dbClass
from HardwareProtocol import Oven_7, Oven_8, Wdj_7, Wdj_8, Volt_7, Volt_8, eLoad, MFC
import socket
import signal
import time
from datetime import datetime
import logging


class myConfig(object):
    def setConfig(self, type=None, cellid=None, ip=None, port=None, addr=None, boxid=None, chnnum=None, cmd=None,
                  plan=None, timeout=1, waittime=1, length=1000, senddata=None, recvdata=None, testid=None,
                  planid=None, gastype=None, protocolversion=None, gasfullscale=None, dbID=None):
        self.type = type
        self.cellid = cellid
        self.ip = ip
        self.port = port
        self.boxid = boxid
        self.cmd = cmd
        self.chnnum = chnnum
        self.plan = plan
        self.timeout = timeout
        self.waittime = waittime
        self.length = length
        self.addr = addr
        self.senddata = senddata
        self.recvdata = recvdata
        self.testid = testid
        self.planid = planid
        self.gastype = gastype
        self.protocolversion = protocolversion
        self.gasfullscale = gasfullscale
        self.dbID = dbID  # 电炉、温度计、电压表对应字段的编号


class socketConnect(object):

    def __init__(self):
        while True:
            try:
                self.db = dbClass("db_config.json")
                self.db_backup = dbClass("backup_db_config.json")
                break
            except Exception as e:
                logging.critical(str(e) + "......创建数据库连接过程中出错,打不开配置文件.....")
                # todo 需要报警，检查数据库连接

    def checksum(self, data):
        # 为从电子负载发出的数据包计算校验和
        csum = 0
        length = data[2] + (data[3] << 8)
        for i in range(length - 2):
            csum = csum + data[4 + i]
        return csum

    def buildCmdMessage(self, config):
        # 若正常，则返回的是命令；若不正常，则直接返回None
        if config.type == 'box':
            load = eLoad(boxid=config.boxid, chnnum=config.chnnum, plan=config.plan)
            if config.cmd == 'start':
                cmd = load.buildcmd("start")
                return cmd
            elif config.cmd == 'stop':
                cmd = load.buildcmd("stop")
                return cmd
            elif config.cmd == 'resume':
                cmd = load.buildcmd("resume")
                return cmd
            elif config.cmd == 'pause':
                cmd = load.buildcmd("pause")
                return cmd
            elif config.cmd == 'read':
                cmd = load.buildcmd("read")
                return cmd
            else:
                logging.error("构建电子负载命令时出错: unknown config.cmd")
                return None

        elif config.type == 'oven':
            if config.protocolversion == '7':
                o = Oven_7(addr=config.addr)
            elif config.protocolversion == '8':
                o = Oven_8(addr=config.addr)
            else:
                logging.error('构建电炉温控器命令时出错：unknown protocol version')
                return None

            if config.cmd == "start":
                if config.protocolversion == '7':
                    cmd = o.buildcmd("r/h/s", "set", 0)
                elif config.protocolversion == '8':
                    cmd = o.buildcmd("Srun", "set", 0)
                else:
                    cmd = None
                return cmd
            elif config.cmd == "stop":
                cmd_list = []
                if config.protocolversion == '7':
                    cmd = o.buildcmd("r/h/s", "set", 12)
                    cmd_list.append(cmd)
                    cmd = o.buildcmd("SV/SteP", "set", 1)
                    cmd_list.append(cmd)
                    return cmd_list
                elif config.protocolversion == '8':
                    cmd = o.buildcmd("Srun", "set", 1)
                    cmd_list.append(cmd)
                    cmd = o.buildcmd("STEP", "set", 1)
                    cmd_list.append(cmd)
                    return cmd_list
                else:
                    return None
            elif config.cmd == "resume":
                if config.protocolversion == '7':
                    cmd = o.buildcmd("r/h/s", "set", 0)
                elif config.protocolversion == '8':
                    cmd = o.buildcmd("Srun", "set", 0)
                else:
                    cmd = None
                return cmd
            elif config.cmd == "pause":
                if config.protocolversion == '7':
                    cmd = o.buildcmd("r/h/s", "set", 4)
                elif config.protocolversion == '8':
                    cmd = o.buildcmd("Srun", "set", 2)
                else:
                    cmd = None
                return cmd
            elif config.cmd == "read":
                if config.protocolversion == '7':
                    cmd = o.buildcmd("SV/SteP", "read")
                elif config.protocolversion == '8':
                    cmd = o.buildcmd("SV", "read")
                else:
                    cmd = None
                return cmd
            elif config.cmd == "setplan":
                i = 1
                cmd_list = []
                for step in config.plan:
                    cmd_list.append(o.buildcmd("C" + str(i), "set", int(step["T"] * 10)))
                    cmd_list.append(o.buildcmd("t" + str(i), "set", int(step["time"])))
                    i = i + 1
                return cmd_list
            else:
                logging.error('构建电炉温控器命令时出错：unknown config.cmd')
                return None

        elif config.type == 'wdj':
            if config.protocolversion == '7':
                w = Wdj_7(addr=config.addr)
            elif config.protocolversion == '8':
                w = Wdj_8(addr=config.addr)
            else:
                logging.error('构建温度巡检仪命令时出错：unknown protocol version')
                return None

            if config.cmd == "read":
                if config.protocolversion == '7':
                    cmd = w.buildcmd("SV/SteP", "read")
                elif config.protocolversion == '8':
                    cmd = w.buildcmd("SV", "read")
                else:
                    cmd = None
                return cmd
            else:
                logging.error('构建温度巡检仪命令时出错：unknown config.cmd')
                return None

        elif config.type == 'volt':
            if config.protocolversion == '7':
                v = Volt_7(addr=config.addr)
            elif config.protocolversion == '8':
                v = Volt_8(addr=config.addr)
            else:
                logging.error('构建温度巡检仪命令时出错：unknown protocol version')
                return None

            if config.cmd == "read":
                if config.protocolversion == '7':
                    cmd = v.buildcmd("SV/SteP", "read")
                elif config.protocolversion == '8':
                    cmd = v.buildcmd("SV", "read")
                else:
                    cmd = None
                return cmd
            else:
                logging.error('构建温度巡检仪命令时出错：unknown config.cmd')
                return None

        elif config.type == 'gas':
            mfc = MFC(config.addr)
            if config.cmd == 'set':
                # value=0x4000~0xC000
                config.plan = int(config.plan / config.gasfullscale * (0xc000 - 0x4000)) + 0x4000
                cmd = mfc.buildcmd(type="SetDigitalSetpoint", value=config.plan)
                return cmd
            elif config.cmd == 'read':
                cmd = mfc.buildcmd(type="ReadFlow")
                return cmd
            else:
                logging.error("构建流量计命令时出错：unknown config.cmd")
                return None

        # elif config.type == 'wdj':
        #     cmd = bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x08, 0x44, 0x0C])
        #     return cmd

        else:
            logging.error("构建命令时出错：unknown config.type")
            return None

    # 若不正常，则直接返回None
    def sendCmdMessage(self, config):
        if config.senddata is None:
            logging.error('待发送命令为None，失败！')
            return None
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(config.timeout)
            s.connect((config.ip, config.port))
            try:
                logging.info('连接' + config.type + '成功！ip:' + config.ip + '  port:' + str(config.port))
                s.send(config.senddata)
                try:
                    time.sleep(config.waittime)
                    recvdata = s.recv(config.length)
                    s.close()
                    return recvdata
                except:  # 接收数据失败
                    logging.error('发送命令后无响应，接收数据超时！')
                    s.close()
                    return None
            except:  # 读取数据失败
                logging.error('发送命令失败，请检查网络连接！')
                return None
        except:  # 建立连接失败
            logging.error('连接' + config.type + '失败！ip:' + config.ip + '  port:' + str(config.port))
            return None

    def sendCmdMessageRepeat(self, config):
        if config.senddata is None:
            logging.error('待发送命令为None，失败！')
            return None
        data = self.sendCmdMessage(config)
        i = 0
        while data is None and i < 0:
            i = i + 1
            logging.error('没有收到返回数据，重新尝试，第' + str(i) + '次')
            data = self.sendCmdMessage(config)
            if data is not None:
                return data
        return data

    def mainProcess(self):
        config = myConfig()
        cellPlan = []
        while True:
            time.sleep(1)
            logging.debug('--------start main process loop--------')
            # 1.查询数据库，提取出需要进行操作的电炉子，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 2.查询数据库，提取出需要进行操作的电池，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 3.查询数据库，提取需要进行操作的流量计，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 4.查询bigtestinfotable，提取出正在运行执行的Test对应的电池、电炉、流量计、温度计、电压表
            # 5.查询数据，更新实时数据表与历史数据表

            ovenUnderHandle = self.db.getOvenUnderHandle()  # 获取待处理的炉子
            cellsUnderHandle = self.db.getCellsUnderHandle()  # 获取待处理的电池测试组
            lljUnderHandle = self.db.getLljUnderHandle()  # 获取待处理的流量计
            # 炉子控制的主逻辑
            for i in ovenUnderHandle:
                # 温控器
                if i['currState'] == 'stop' and i['nextState'] == 'start':
                    # 首先设置方案
                    ovenPlan = self.db.getOvenTestPlan(i)
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="setplan", plan=ovenPlan,
                                     addr=i["Addr"], protocolversion=i["protocolVersion"])
                    senddata = self.buildCmdMessage(config)

                    for j in senddata:
                        config.senddata = j
                        config.recvdata = self.sendCmdMessageRepeat(config)
                        if config.recvdata is None:
                            logging.error('设置温控器升温方式时没有收到回复')
                            time.sleep(10)
                            # todo 需要报警，检查网络连接
                            break

                    # 然后启动电炉
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="start", plan=ovenPlan,
                                     addr=i["Addr"], protocolversion=i["protocolVersion"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'start' and i['nextState'] == 'pause':
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="pause", addr=i["Addr"],
                                     protocolversion=i["protocolVersion"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'start' and i['nextState'] == 'stop':
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="stop", addr=i["Addr"],
                                     protocolversion=i["protocolVersion"])
                    senddata = self.buildCmdMessage(config)
                    for j in senddata:
                        config.senddata = j
                        config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'pause' and i['nextState'] == 'start':
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="start", addr=i["Addr"],
                                     protocolversion=i["protocolVersion"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'pause' and i['nextState'] == 'stop':
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="stop", addr=i["Addr"],
                                     protocolversion=i["protocolVersion"])
                    senddata = self.buildCmdMessage(config)
                    for j in senddata:
                        config.senddata = j
                        config.recvdata = self.sendCmdMessageRepeat(config)
                        if config.recvdata is None:
                            break
                    self.updateOvenState(config, i["ID"])

                else:
                    logging.error("处理待处理温控器时出错：unknown currstate & nextstate")

            # 流量计主逻辑
            for i in lljUnderHandle:
                settingValue = i['nextState']
                if settingValue > i["fullScale"]:
                    # todo需要报警
                    logging.error('流量计写入值超量程！')
                    continue
                config.setConfig(type="gas", ip=i["IP"], port=i["PortNum"], cmd="set", addr=i['Addr'],
                                 plan=settingValue, gasfullscale=i["fullScale"])
                config.senddata = self.buildCmdMessage(config)
                config.recvdata = self.sendCmdMessageRepeat(config)
                self.updateGasState(config, i["type"], i["ID"])

            # 电子负载控制的主逻辑
            for i in cellsUnderHandle:
                COM = (self.db.getCellsComponetCOM(i))[0]
                if (i['currState'] == "start") and (i['nextState'] == "pause"):
                    logging.debug('尝试暂停电子负载')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=COM['Addr'],
                                     chnnum=i['chnNum'],
                                     cmd='pause')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateCellBoxState(config)

                elif (i['nextState'] == "stop"):
                    logging.debug('尝试停止电子负载')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=COM['Addr'],
                                     chnnum=i['chnNum'],
                                     cmd='stop')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateCellBoxState(config)

                elif (i['currState'] == "stop") and (i['nextState'] == "start"):
                    logging.debug('尝试启动电子负载')
                    cellplan = self.db.getCellsTestPlan(i)
                    ## todo check cell plan
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=COM['Addr'],
                                     chnnum=i['chnNum'],
                                     cmd='start',
                                     plan=cellplan,
                                     waittime=2,
                                     length=4000)
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateCellBoxState(config)

                elif (i['currState'] == "pause") and (i['nextState'] == "resume"):
                    logging.debug('尝试继续电子负载')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=COM['Addr'],
                                     chnnum=i['chnNum'],
                                     cmd='resume')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    self.updateCellBoxState(config)

                else:
                    logging.error("处理待处理通道时出错：unknown currstate & nextstate")

            # 以上程序执行完之后，所有的控制命令均已处理，接下来处理读数命令
            # 首先获取正在进行的父测试，可以得知该测试所对应的设备信息，然后逐个查询

            testUnderHandle = self.db.getUncompleteBigTest()
            for i in testUnderHandle:
                if i["cellID_id"] is not None:
                    i["testID_id"] = self.db.getTestIDfromCell(i["cellID_id"])[0]["testID_id"]
                else:
                    i["testID_id"] = None
            for i in testUnderHandle:
                # 依次读取各组件的信息，并更新数据表，最后插入历史数据表
                AllData = {}
                # 此处逻辑为，若该测试中包含某设备，则查询该设备的数据，并将其入库
                # 若无该设备，则依然入库，但所有值均为0
                AllData.update({
                    "bigTestID_id": i["id"],
                    "testID_id": i["testID_id"],
                })
                if i["boxID_id"] is not None:
                    logging.debug('读取电子负载数据')
                    COM = self.db.getCellsComponetCOM({"cellID_id": i['cellID_id']})[0]
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=COM['Addr'],
                                     cmd='read',
                                     chnnum=i['chnNum'],
                                     waittime=2,
                                     length=4000)
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'mode': 0, 'T': 0, 'r': 0,
                                                                          'overOutDataFlag': 0, 'qA': 0,
                                                                          'tc': 0, 'q': 0, 'i': 0, 'resultDataFlag': 0,
                                                                          'chMasterSlaveFlag': 0, 'ta': 0,
                                                                          'k': 0,
                                                                          'celldata_time': datetime.now().strftime(
                                                                              "%Y-%m-%d %H:%M:%S"),
                                                                          'chStateCode': 0, 'detailDataFlag': 0,
                                                                          'chState': 0, 'powerDownFlag': 0, 'n': 0,
                                                                          'u': 0})
                else:
                    AllData.update({'mode': 0, 'T': 0, 'r': 0, 'overOutDataFlag': 0, 'qA': 0, 'tc': 0, 'q': 0,
                                    'i': 0, 'resultDataFlag': 0, 'chMasterSlaveFlag': 0, 'ta': 0, 'k': 0,
                                    'celldata_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'chStateCode': 0,
                                    'detailDataFlag': 0, 'chState': 0, 'powerDownFlag': 0, 'n': 0, 'u': 0})

                if i["AIRID_id"] is not None:
                    logging.debug('读取Air-MFC数据')
                    COM = self.db.getGasCOM('AIR', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="AIR",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qAIR': 0, 'tAIR': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qAIR': 0, 'tAIR': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["H2ID_id"] is not None:
                    logging.debug('读取H2-MFC数据')
                    COM = self.db.getGasCOM('H2', i)[0]
                    config.setConfig(type='gas',
                                     ip=COM['IP'],
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="H2",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qH2': 0, 'tH2': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qH2': 0, 'tH2': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["N2ID_id"] is not None:
                    logging.debug('读取N2-MFC数据')
                    COM = self.db.getGasCOM('N2', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="N2",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qN2': 0, 'tN2': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qN2': 0, 'tN2': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["CH4ID_id"] is not None:
                    logging.debug('读取CH4-MFC数据')
                    COM = self.db.getGasCOM('CH4', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="CH4",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qCH4': 0, 'tCH4': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qCH4': 0, 'tCH4': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["CO2ID_id"] is not None:
                    logging.debug('读取CO2-MFC数据')
                    COM = self.db.getGasCOM('CO2', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="CO2",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qCO2': 0, 'tCO2': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qCO2': 0, 'tCO2': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["H2OID_id"] is not None:
                    logging.debug('读取H2O-MFC数据')
                    COM = self.db.getGasCOM('H2O', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="H2O",
                                     gasfullscale=COM["fullScale"]
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessageRepeat(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {'qH2O': 0, 'tH2O': datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")})
                else:
                    AllData.update({'qH2O': 0, 'tH2O': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                for ID in range(4):
                    if i["oven" + str(ID) + "ID_id"] is not None:
                        logging.debug('读取温控器' + str(ID) + '数据')
                        COM = self.db.getOvenCOM(i, ID)[0]
                        config.setConfig(type='oven',
                                         cellid=i['cellID_id'],
                                         chnnum=i['chnNum'],
                                         boxid=i['boxID_id'],
                                         ip=COM['IP'],
                                         port=COM['PortNum'],
                                         addr=COM['Addr'],
                                         cmd='read',
                                         dbID=ID,
                                         protocolversion=COM["protocolVersion"]
                                         )
                        config.senddata = self.buildCmdMessage(config)
                        config.recvdata = self.sendCmdMessageRepeat(config)
                        datadict = self.updateCellRealData(config)
                        AllData.update(datadict if datadict is not None
                                       else {'sTc' + str(ID): 0, 'Tc' + str(ID): 0,
                                             'tTc' + str(ID): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    else:
                        AllData.update(
                            {'sTc' + str(ID): 0, 'Tc' + str(ID): 0,
                             'tTc' + str(ID): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["wdjID_id"] is not None:
                    logging.debug('读取温度巡检仪数据')
                    COM = self.db.getWdjCOM(i)[0]
                    chaNum = COM['totalChnNum']
                    for chn in range(chaNum):
                        config.setConfig(type='wdj',
                                         ip=COM['IP'],
                                         cellid=i['cellID_id'],
                                         chnnum=i['chnNum'],
                                         boxid=i['boxID_id'],
                                         port=COM['PortNum'],
                                         addr=COM['Addr'] + chn,
                                         cmd='read',
                                         dbID=chn,
                                         protocolversion=COM["protocolVersion"]
                                         )
                        config.senddata = self.buildCmdMessage(config)
                        config.recvdata = self.sendCmdMessageRepeat(config)
                        datadict = self.updateCellRealData(config)
                        AllData.update(datadict if datadict is not None
                                       else {'Tm' + str(chn): 0,
                                             'tTm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    for chn in range(chaNum, 20):
                        AllData.update(
                            {'Tm' + str(chn): 0, 'tTm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                else:
                    for chn in range(20):
                        AllData.update(
                            {'Tm' + str(chn): 0, 'tTm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                if i["voltID_id"] is not None:
                    logging.debug('读取电压巡检仪数据')
                    COM = self.db.getVoltCOM(i)[0]
                    chaNum = COM['totalChnNum']
                    for chn in range(chaNum):
                        config.setConfig(type='volt',
                                         ip=COM['IP'],
                                         cellid=i['cellID_id'],
                                         chnnum=i['chnNum'],
                                         boxid=i['boxID_id'],
                                         port=COM['PortNum'],
                                         addr=COM['Addr'] + chn,
                                         cmd='read',
                                         dbID=chn,
                                         protocolversion=COM["protocolVersion"]
                                         )
                        config.senddata = self.buildCmdMessage(config)
                        config.recvdata = self.sendCmdMessageRepeat(config)
                        datadict = self.updateCellRealData(config)
                        AllData.update(datadict if datadict is not None
                                       else {'Vm' + str(chn): 0,
                                             'tVm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    for chn in range(chaNum, 20):
                        AllData.update(
                            {'Vm' + str(chn): 0, 'tVm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                else:
                    for chn in range(20):
                        AllData.update(
                            {'Vm' + str(chn): 0, 'tVm' + str(chn): datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

                # if i["cellID_id"] is not None:
                #     testid = self.db.getTestIDfromCell(i["cellID_id"])[0]["testID_id"]
                # else:
                #     testid = None
                # AllData.update({
                #     "bigTestID_id": i["id"],
                #     "testID_id": testid,
                # })
                logging.debug('..................update history........................')
                self.insertHistoryData(AllData)

    def updateCellBoxState(self, config):
        newstate = config.cmd
        cellid = config.cellid
        data = config.recvdata
        DataDict = {}
        if data is None:
            logging.error("更新电子负载状态出错，没有返回数据！")
            return None
        if newstate == 'start':
            if len(data) == 46:
                if data[7] == 0x06:
                    DataDict['currState'] = 'start'
                    self.db.updateCellRealData(cellid, DataDict)
                else:
                    logging.error("更新电子负载状态出错，返回数据命令号字段(data[7]==0x06)不对！")
        elif newstate == 'pause':
            if len(data) == 46:
                if data[7] == 0x08:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'pause'
                        self.db.updateCellRealData(cellid, DataDict)
                    else:
                        logging.error("更新电子负载状态出错，返回数据字段(data[8，9]==0x00)不对！")
                else:
                    logging.error("更新电子负载状态出错，返回数据命令号字段(data[7]==0x08)不对！")
        elif newstate == 'resume':
            if len(data) == 46:
                if data[7] == 0x08:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'start'
                        DataDict['nextState'] = 'start'
                        self.db.updateCellRealData(cellid, DataDict)
                    else:
                        logging.error("更新电子负载状态出错，返回数据字段(data[8，9]==0x00)不对！")
                else:
                    logging.error("更新电子负载状态出错，返回数据命令号字段(data[7]==0x08)不对！")
        elif newstate == 'stop':
            if len(data) == 46:
                if data[7] == 0x07:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'stop'
                        self.db.updateCellRealData(cellid, DataDict)
                    else:
                        logging.error("更新电子负载状态出错，返回数据字段(data[8，9]==0x00)不对！")
                else:
                    logging.error("更新电子负载状态出错，返回数据命令号字段(data[7]==0x08)不对！")
        else:
            logging.error("更新电子负载状态出错! unknown newstate(config.cmd)")

    def updateGasState(self, config, gastype, MFCid):
        data = config.recvdata
        if data is None:
            logging.error("更新MFC状态出错，没有返回数据！")
            return None
        if data[0] == 0x06:  # 帧头校验
            DataDict = {}
            DataDict['currState'] = config.plan
            self.db.updateGasTable(gastype, DataDict, MFCid)
            return DataDict
        else:
            logging.error("更新MFC状态出错，返回帧结构不对！")
            return None

    # if ((data[0] == ord(config.addr)) and data[-1] == 0x0D):  # 帧头帧尾校验
    #     data = data.decode()
    #     data = data.split()
    #     if (len(data) == 7 and config.cmd == 'set'):  # 数据长度校验
    #         DataDict = {}
    #         DataDict['currState'] = config.plan
    #         db.updateGasTable(gastype, DataDict, MFCid)
    #         return DataDict
    #     else:
    #         print("update gas state: wrong frame")
    #         return None
    # else:
    #     print("update gas state: wrong frame")
    #     return None

    def updateOvenState(self, config, Ovenid):
        data = config.recvdata
        if data is None:
            logging.error("更新温控器状态出错，没有返回数据！")
            return None
        if len(data) == 10:  # 帧长校验
            DataDict = {}
            DataDict['currState'] = config.cmd
            self.db.updateOvenTable(DataDict, Ovenid)
            return DataDict
        else:
            logging.error("更新温控器状态出错，返回数据错误！")
            return None

    def updateCellRealData(self, config):
        cmd = config.cmd
        data = config.recvdata
        if data is None:
            logging.error("更新实时测试数据状态出错，没有返回数据！")
            return None
        cellid = config.cellid
        boxid = config.boxid
        chnnum = config.chnnum
        logging.debug("更新实时测试数据...type:" + str(config.type) + "...cmd:" + str(cmd))
        if config.type == 'box':
            if cmd == 'read':
                if ((data[0] == 0xAA) and (data[1] == 0x55) and (data[-1] == 0xAA) and (data[-2] == 0x55)):  # 帧头帧尾校验
                    if ((len(data) == data[2] + (data[3] << 8) + 6) and len(data) == 3471):  # 数据长度校验
                        if data[6] == boxid:
                            # if data[6] == 0x00:
                            logging.debug("更新电子负载实时数据成功")
                            DataDict = {}
                            i = chnnum
                            DataDict['chState'] = data[11 + i * 54 + 1]
                            DataDict['chStateCode'] = (data[11 + i * 54 + 2] << 8) + data[11 + i * 54 + 3]
                            DataDict['chMasterSlaveFlag'] = data[11 + i * 54 + 4]
                            DataDict['n'] = data[11 + i * 54 + 5]
                            DataDict['k'] = (data[11 + i * 54 + 6]) + (data[11 + i * 54 + 7] << 8)
                            DataDict['mode'] = data[11 + i * 54 + 8]

                            DataDict['tc'] = (data[11 + i * 54 + 10] << 24) + (data[11 + i * 54 + 11] << 16) + (
                                    data[11 + i * 54 + 12] << 8) + (data[11 + i * 54 + 13])
                            DataDict['ta'] = (data[11 + i * 54 + 14] << 24) + (data[11 + i * 54 + 15] << 16) + (
                                    data[11 + i * 54 + 16] << 8) + (data[11 + i * 54 + 17])

                            DataDict['u'] = (data[11 + i * 54 + 19] << 24) + (data[11 + i * 54 + 20] << 16) + (
                                    data[11 + i * 54 + 21] << 8) + (data[11 + i * 54 + 22])
                            DataDict['i'] = (data[11 + i * 54 + 23] << 24) + (data[11 + i * 54 + 24] << 16) + (
                                    data[11 + i * 54 + 25] << 8) + (data[11 + i * 54 + 26])
                            DataDict['q'] = (data[11 + i * 54 + 27] << 24) + (data[11 + i * 54 + 28] << 16) + (
                                    data[11 + i * 54 + 29] << 8) + (data[11 + i * 54 + 30])
                            DataDict['qA'] = (data[11 + i * 54 + 31] << 24) + (data[11 + i * 54 + 32] << 16) + (
                                    data[11 + i * 54 + 33] << 8) + (data[11 + i * 54 + 34])
                            DataDict['T'] = (data[11 + i * 54 + 35] << 24) + (data[11 + i * 54 + 36] << 16) + (
                                    data[11 + i * 54 + 37] << 8) + (data[11 + i * 54 + 38])
                            DataDict['r'] = (data[11 + i * 54 + 39] << 24) + (data[11 + i * 54 + 40] << 16) + (
                                    data[11 + i * 54 + 41] << 8) + (data[11 + i * 54 + 42])

                            DataDict['detailDataFlag'] = (data[11 + i * 54 + 43] << 8) + data[11 + i * 54 + 44]
                            DataDict['resultDataFlag'] = (data[11 + i * 54 + 45] << 8) + data[11 + i * 54 + 46]
                            DataDict['overOutDataFlag'] = (data[11 + i * 54 + 47] << 8) + data[11 + i * 54 + 48]
                            DataDict['powerDownFlag'] = (data[11 + i * 54 + 49] << 8)

                            DataDict['celldata_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.db.updateCellRealData(cellid, DataDict)
                            return DataDict
                        else:
                            logging.error("更新电子负载实时数据失败！unknown box_id(config.boxid)")
                            return None
                    else:
                        logging.error("更新电子负载实时数据失败！wrong data length")
                        return None
                else:
                    logging.error("更新电子负载实时数据失败！wrong frame")
                    return None
            else:
                logging.error("更新电子负载实时数据失败！unknown cmd(config.cmd)")
                return None
        elif config.type == "gas1":
            if ((data[0] == ord(config.addr)) and data[-1] == 0x0D):  # 帧头帧尾校验
                data = data.decode()
                data = data.split()
                if (len(data) == 7):  # 数据长度校验
                    GasDataDict = {}
                    if config.gastype == 'H2':
                        GasDataDict['qH2'] = float(data[4])
                        GasDataDict['tH2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'N2':
                        GasDataDict['qN2'] = float(data[4])
                        GasDataDict['tN2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CO2':
                        GasDataDict['qCO2'] = float(data[4])
                        GasDataDict['tCO2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CH4':
                        GasDataDict['qCH4'] = float(data[4])
                        GasDataDict['tCH4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'AIR':
                        GasDataDict['qAIR'] = float(data[4])
                        GasDataDict['tAIR'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'H2O':
                        GasDataDict['qH2O'] = float(data[4])
                        GasDataDict['tH2O'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    else:
                        print("update_cell_data_gas: unknown gastype")
                        return None
                else:
                    print("update_cell_data_gas: wrong data length")
                    return None
            else:
                print("update_cell_data_gas: wrong frame")
                return None
        elif config.type == "gas":
            if data[0] == 0x06:  # 帧头校验
                if (len(data) == 12):  # 数据长度校验
                    GasDataDict = {}
                    data = (data[8] + data[9] << 8 - 0x4000) / (0xc000 - 0x4000) * config.gasfullscale
                    if config.gastype == 'H2':
                        GasDataDict['qH2'] = data
                        GasDataDict['tH2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'N2':
                        GasDataDict['qN2'] = data
                        GasDataDict['tN2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CO2':
                        GasDataDict['qCO2'] = data
                        GasDataDict['tCO2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CH4':
                        GasDataDict['qCH4'] = data
                        GasDataDict['tCH4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'AIR':
                        GasDataDict['qAIR'] = data
                        GasDataDict['tAIR'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'H2O':
                        GasDataDict['qH2O'] = data
                        GasDataDict['tH2O'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    else:
                        logging.error("更新MFC实时数据失败：unknown gastype")
                        return None
                else:
                    logging.error("更新MFC实时数据失败：wrong data length")
                    return None
            else:
                logging.error("更新MFC实时数据失败： wrong frame header")
                return None
        elif config.type == "oven":
            if len(data) == 10:  # 帧长校验
                PV = data[0] + (data[1] << 8)
                SV = data[2] + (data[3] << 8)
                MV = data[4] + (data[5] << 8)
                value = data[6] + (data[7] << 8)
                checksum = PV + SV + MV + value + config.addr
                checksumLO = checksum & 0xff
                checksumHI = (checksum & 0xff00) >> 8
                if data[8] == checksumLO and data[9] == checksumHI:
                    PV = PV if PV < 0x8000 else -(((~PV) & 0xffff) + 1)
                    SV = SV if SV < 0x8000 else -(((~SV) & 0xffff) + 1)
                    MV = data[4] if data[4] < 0x80 else ~data[4]
                    value = value if value < 0x8000 else -(((~value) & 0xffff) + 1)
                    ALARM = data[5]
                    HIAL = bool(ALARM & 0x01)
                    LoAL = bool(ALARM & 0x02)
                    dHAL = bool(ALARM & 0x04)
                    dLAL = bool(ALARM & 0x08)
                    orAL = bool(ALARM & 0x10)
                    AL1 = not bool(ALARM & 0x20)
                    AL2 = not bool(ALARM & 0x40)

                    OvenDataDict = {'Tc' + str(config.dbID): PV / 10}
                    OvenDataDict['tTc' + str(config.dbID)] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    OvenDataDict['sTc' + str(config.dbID)] = 0
                    self.db.updateCellRealData(cellid, OvenDataDict)
                    return OvenDataDict
                else:
                    logging.error("更新温控器数据失败：wrong frame")
                    return None
            else:
                logging.error("更新温控器数据失败：wrong data length")
                return None
        elif config.type == "wdj":
            if len(data) == 10:  # 帧长校验
                PV = data[0] + (data[1] << 8)
                SV = data[2] + (data[3] << 8)
                MV = data[4] + (data[5] << 8)
                value = data[6] + (data[7] << 8)
                checksum = PV + SV + MV + value + config.addr
                checksumLO = checksum & 0xff
                checksumHI = (checksum & 0xff00) >> 8
                if data[8] == checksumLO and data[9] == checksumHI:
                    PV = PV if PV < 0x8000 else -(((~PV) & 0xffff) + 1)
                    SV = SV if SV < 0x8000 else -(((~SV) & 0xffff) + 1)
                    MV = data[4] if data[4] < 0x80 else ~data[4]
                    value = value if value < 0x8000 else -(((~value) & 0xffff) + 1)
                    ALARM = data[5]
                    HIAL = bool(ALARM & 0x01)
                    LoAL = bool(ALARM & 0x02)
                    dHAL = bool(ALARM & 0x04)
                    dLAL = bool(ALARM & 0x08)
                    orAL = bool(ALARM & 0x10)
                    AL1 = not bool(ALARM & 0x20)
                    AL2 = not bool(ALARM & 0x40)
                    OvenDataDict = {'Tm' + str(config.dbID): PV / 10}
                    OvenDataDict['tTm' + str(config.dbID)] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.db.updateCellRealData(cellid, OvenDataDict)
                    return OvenDataDict
                else:
                    logging.error("更新温度巡检仪数据失败：wrong frame")
                    return None
            else:
                logging.error("更新温度巡检仪数据失败：wrong data length")
                return None
        elif config.type == "volt":
            if len(data) == 10:  # 帧长校验
                PV = data[0] + (data[1] << 8)
                SV = data[2] + (data[3] << 8)
                MV = data[4] + (data[5] << 8)
                value = data[6] + (data[7] << 8)
                checksum = PV + SV + MV + value + config.addr
                checksumLO = checksum & 0xff
                checksumHI = (checksum & 0xff00) >> 8
                if data[8] == checksumLO and data[9] == checksumHI:
                    PV = PV if PV < 0x8000 else -(((~PV) & 0xffff) + 1)
                    SV = SV if SV < 0x8000 else -(((~SV) & 0xffff) + 1)
                    MV = data[4] if data[4] < 0x80 else ~data[4]
                    value = value if value < 0x8000 else -(((~value) & 0xffff) + 1)
                    ALARM = data[5]
                    HIAL = bool(ALARM & 0x01)
                    LoAL = bool(ALARM & 0x02)
                    dHAL = bool(ALARM & 0x04)
                    dLAL = bool(ALARM & 0x08)
                    orAL = bool(ALARM & 0x10)
                    AL1 = not bool(ALARM & 0x20)
                    AL2 = not bool(ALARM & 0x40)
                    OvenDataDict = {'Vm' + str(config.dbID): PV / 10}
                    OvenDataDict['tVm' + str(config.dbID)] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.db.updateCellRealData(cellid, OvenDataDict)
                    return OvenDataDict
                else:
                    logging.error("更新电压巡检仪数据失败：wrong frame")
                    return None
            else:
                logging.error("更新电压巡检仪数据失败：wrong data length")
                return None
        # elif config.type == "wdj":
        #     if ((data[0] == 1) and (data[1] == 0x03) and (data[2] == 0x10)):  # 帧头帧尾校验
        #         if (len(data) == data[2] + 5):  # 数据长度校验
        #             wdjDataDict = {}
        #             wdjDataDict['T1'] = ((data[3] << 8) + data[4]) / 10
        #             wdjDataDict['T2'] = ((data[5] << 8) + data[6]) / 10
        #             wdjDataDict['T3'] = ((data[7] << 8) + data[8]) / 10
        #             wdjDataDict['T4'] = ((data[9] << 8) + data[10]) / 10
        #             wdjDataDict['tT1'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             wdjDataDict['tT2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             wdjDataDict['tT3'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             wdjDataDict['tT4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #             db.updateCellRealData(cellid, wdjDataDict)
        #             return wdjDataDict
        #         else:
        #             print("update_cell_data_gas: wrong data length")
        #             return None
        #     else:
        #         print("update_cell_data_wdj: wrong frame")
        #         return None

    def insertHistoryData(self, data):
        self.db.insertHistoryData(data)
        ##todo
        # self.db_backup.insertHistoryData(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(levelname)s] %(message)s',
                        filename='socket.log',
                        filemode='a')
    socketRun = socketConnect()
    socketRun.mainProcess()
