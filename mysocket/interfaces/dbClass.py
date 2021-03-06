# -*- coding: utf-8 -*-
# @Author: wx
# @Date:   2018-05-16 14:18:31
# @Last Modified by:   wx
# @Last Modified time: 2018-06-07 10:50:25

import pymysql
import json
import logging
import time


class dbClass(object):
    """docstring for dbClass"""

    def __init__(self, settings):
        logging.debug('尝试初始化数据库')
        try:
            with open(settings, 'r') as f:
                filetext = f.read()
        except Exception as e:
            logging.error(str(e))
            logging.error('初始化数据库时出错，打不开配置文件')
            raise e

        configJson = json.loads(filetext)
        self.host = configJson['host']
        self.port = int(configJson['port'])
        self.user = configJson['user']
        self.passwd = configJson['passwd']
        self.db = configJson['db']
        self.cellDeviceTable = configJson['cellDeviceTable']
        self.boxDeviceTable = configJson['boxDeviceTable']
        self.cellDeviceTable = configJson["cellDeviceTable"]
        self.H2DeviceTable = configJson["H2DeviceTable"]
        self.H2ODeviceTable = configJson["H2ODeviceTable"]
        self.CO2DeviceTable = configJson["CO2DeviceTable"]
        self.CH4DeviceTable = configJson["CH4DeviceTable"]
        self.N2DeviceTable = configJson["N2DeviceTable"]
        self.AIRDeviceTable = configJson["AIRDeviceTable"]
        self.wdjDeviceTable = configJson["wdjDeviceTable"]
        self.voltDeviceTable = configJson["voltDeviceTable"]
        self.ovenDeviceTable = configJson["ovenDeviceTable"]
        self.ovenPlanTable = configJson["ovenPlanTable"]
        self.ovenPlanDetailTable = configJson["ovenPlanDetailTable"]
        self.cellPlanTable = configJson["cellPlanTable"]
        self.cellPlanDetailTable = configJson["cellPlanDetailTable"]
        self.BigTestInfoTable = configJson["BigTestInfoTable"]
        self.testInfoTable = configJson["testInfoTable"]
        self.cellTestRealDataTable = configJson["cellTestRealDataTable"]
        self.eventTable = configJson["eventTable"]
        self.cellTestHistoryDataTable = configJson["cellTestHistoryDataTable"]

    def updateCellDeviceTable(self, boxid, chnNum, datadict):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        ROWstr = ''
        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','
        ROWstr = ROWstr[:-1]
        ROWstr = ROWstr + ' '
        sql = 'update ' + self.cellDeviceTable + ' SET ' + ROWstr + 'where (boxID_id = ' + str(
            boxid) + ') and ' + '(chnNum = ' + str(chnNum) + ')'
        i = 0
        while True:
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()

    def updateCellDeviceTable_Gas_Temp(self, cellid, datadict):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        ROWstr = ''
        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','

        ROWstr = ROWstr[:-1]
        ROWstr = ROWstr + ' '
        sql = 'update ' + self.cellDeviceTable + ' SET ' + ROWstr + 'where (cellID = ' + str(cellid) + ')'
        i = 0
        while True:
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()

    def executeGetSQL(self, sql, keys):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        r_list = []
        i = 0
        while True:
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for i in result:
                    data = {}
                    for j in range(0, len(keys)):
                        data[keys[j]] = i[j]
                    r_list.append(data)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行get-sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行get-sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()
        return r_list

    def getCellsUnderHandle(self):
        logging.debug("获取待处理的电子负载通道")
        keys = ["cellID_id", "boxID_id", "testID_id", "bigTestID_id", "chnNum", "currState", "nextState"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellTestRealDataTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        logging.debug("获取待处理的电子负载通道：" + str(result))
        return result

    def getCellsTestPlan(self, cell):
        keys = ["planID_id", ]
        sql = 'SELECT planID_id FROM ' + self.testInfoTable + ' WHERE id=' + str(cell["testID_id"])
        result = self.executeGetSQL(sql, keys)
        keys = ["id", "planID_id", "step", "mode", "i", "u", "r", "p", "n", "nStart", "nStop", "nTarget", "tTH", "iTH",
                "uTH", "qTH"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellPlanDetailTable + ' WHERE planID_id=' + str(
            result[0]["planID_id"]) + ' ORDER BY step'
        result = self.executeGetSQL(sql, keys)
        return result

    def getCellsComponetCOM(self, cell):
        keys = ["cellID", "chnNum", "boxID_id"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.cellDeviceTable + " WHERE cellID=" + str(cell["cellID_id"])
        cellDevice = self.executeGetSQL(sql, keys)[0]

        keys = ["ID", "IP", "PortNum", "Addr", "totalChnNum"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.boxDeviceTable + " WHERE ID=" + str(cellDevice["boxID_id"])
        data = self.executeGetSQL(sql, keys)
        data[0]["chnNum"] = cellDevice["chnNum"]
        data[0]["cellID"] = cellDevice["cellID"]
        return data

    def getGasCOM(self, gtype, llj):
        keys = ["ID", "IP", "PortNum", "Addr", "fullScale"]
        keystr = ",".join(keys)
        if gtype == "H2":
            sql = "SELECT " + keystr + " FROM " + self.H2DeviceTable + " WHERE ID=" + str(llj["H2ID_id"])
        elif gtype == "N2":
            sql = "SELECT " + keystr + " FROM " + self.N2DeviceTable + " WHERE ID=" + str(llj["N2ID_id"])
        elif gtype == "CH4":
            sql = "SELECT " + keystr + " FROM " + self.CH4DeviceTable + " WHERE ID=" + str(llj["CH4ID_id"])
        elif gtype == "CO2":
            sql = "SELECT " + keystr + " FROM " + self.CO2DeviceTable + " WHERE ID=" + str(llj["CO2ID_id"])
        elif gtype == "AIR":
            sql = "SELECT " + keystr + " FROM " + self.AIRDeviceTable + " WHERE ID=" + str(llj["AIRID_id"])
        elif gtype == "H2O":
            sql = "SELECT " + keystr + " FROM " + self.H2ODeviceTable + " WHERE ID=" + str(llj["H2OID_id"])
        else:
            sql = None
        if sql is None:
            logging.error("SQL语句为空")
            return None
        data = self.executeGetSQL(sql, keys)
        return data

    def getOvenCOM(self, oven, num):
        keys = ["ID", "IP", "PortNum", "Addr", "protocolVersion"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.ovenDeviceTable + " WHERE ID=" + str(
            oven["oven" + str(num) + "ID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getWdjCOM(self, wdj):
        keys = ["ID", "IP", "PortNum", "Addr", "totalChnNum", "protocolVersion"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.wdjDeviceTable + " WHERE ID=" + str(wdj["wdjID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getVoltCOM(self, volt):
        keys = ["ID", "IP", "PortNum", "Addr", "totalChnNum", "protocolVersion"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.voltDeviceTable + " WHERE ID=" + str(volt["voltID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getOvenUnderHandle(self):
        logging.debug("获取待处理温控器")
        keys = ["ID", "currState", "nextState", "IP", "PortNum", "Addr", "ovenPlanID_id", "protocolVersion"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.ovenDeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        logging.debug("获取待处理温控器:" + str(result))
        return result

    def getLljUnderHandle(self):
        logging.debug("获取待处理MFC")
        keys = ["ID", "currState", "nextState", "IP", "PortNum", "Addr", "fullScale"]
        keystr = ",".join(keys)
        data = []
        tables = {'H2': self.H2DeviceTable, 'N2': self.N2DeviceTable, 'CO2': self.CO2DeviceTable,
                  'CH4': self.CH4DeviceTable, 'AIR': self.AIRDeviceTable, 'H2O': self.H2ODeviceTable}
        for j in tables.keys():
            sql = 'SELECT ' + keystr + ' FROM ' + tables[j] + ' WHERE (currState!=nextState)'
            result = self.executeGetSQL(sql, keys)
            for i in result:
                i["type"] = j
            data = data + result
        logging.debug("获取待处理MFC:" + str(data))
        return data

    def getOvenTestPlan(self, oven):
        keys = ["id", "step", "T", "time", "ovenPlanID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.ovenPlanDetailTable + ' WHERE ovenPlanID_id=' + str(
            oven["ovenPlanID_id"]) + ' ORDER BY step '
        result = self.executeGetSQL(sql, keys)
        return result

    def getUncompleteBigTest(self):
        logging.debug("获取未完成的BigTest")
        keys = ["id", "chnNum", "AIRID_id", "CH4ID_id", "CO2ID_id", "H2ID_id", "H2OID_id", "N2ID_id", "boxID_id",
                "cellID_id", "oven0ID_id", "oven1ID_id", "oven2ID_id", "oven3ID_id", "wdjID_id", "voltID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.BigTestInfoTable + ' WHERE completeFlag=0 '
        result = self.executeGetSQL(sql, keys)
        logging.debug("获取未完成的BigTest:" + str(result))
        return result

    def getTestIDfromCell(self, cellid):
        keys = ["cellID_id", "boxID_id", "chnNum", "bigTestID_id", "testID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellTestRealDataTable + ' WHERE cellID_id=' + str(cellid)
        result = self.executeGetSQL(sql, keys)
        return result

    def executeInsertSQL(self, datadict, table):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        ROWstr = []
        COLstr = ''
        ss = ''
        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            ROWstr.append(datadict[key])
            COLstr = COLstr + key + ','
            ss = ss + '%s' + ','
        COLstr = COLstr[:-1]
        ss = ss[:-1]
        sql = "insert into  " + table + " (" + COLstr + ") values (" + ss + ")"
        i = 0
        while True:
            try:
                cursor.execute(sql, ROWstr)
                dbconnection.commit()
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行insert-sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行insert-sql语句失败,重试中')
        dbconnection.close()

    def insertHistoryData(self, datadict):
        self.executeInsertSQL(datadict, self.cellTestHistoryDataTable)

    def updateGasTable(self, gastype, datadict, MFCid):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        if gastype == "H2":
            table = self.H2DeviceTable
        elif gastype == "CO2":
            table = self.CO2DeviceTable
        elif gastype == "N2":
            table = self.N2DeviceTable
        elif gastype == "AIR":
            table = self.AIRDeviceTable
        elif gastype == "H2O":
            table = self.H2ODeviceTable
        elif gastype == "CH4":
            table = self.CH4DeviceTable
        else:
            logging.error("update gas table: unknown gas type")
            return None
        ROWstr = ''
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','
        ROWstr = ROWstr[:-1]
        sql = 'update ' + table + ' SET ' + ROWstr + ' where ID=' + str(MFCid)
        i = 0
        while True:
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行update-sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行insert-sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()

    def updateOvenTable(self, datadict, Ovenid):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        ROWstr = ''
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','
        ROWstr = ROWstr[:-1]
        sql = 'update ' + self.ovenDeviceTable + ' SET ' + ROWstr + ' where ID=' + str(Ovenid)
        i = 0
        while True:
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行update-sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行insert-sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()

    def updateCellRealData(self, cellid, datadict):
        i = 0
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                               db=self.db, charset="utf8")
                break
            except Exception as e:
                i = i + 1
                logging.error(str(e))
                if i > 10:
                    logging.critical("连接数据库失败!!")
                    return None
                logging.error("无法连接到数据库,host=" + str(self.host) + ",port=" + str(self.port) + ",10秒后重连")
                time.sleep(10)
        cursor = dbconnection.cursor()
        ROWstr = ''

        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','

        ROWstr = ROWstr[:-1]
        ROWstr = ROWstr + ' '
        sql = 'update ' + self.cellTestRealDataTable + ' SET ' + ROWstr + 'where (cellID_id = ' + str(cellid) + ')'
        i = 0
        while True:
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                i = i + 1
                logging.error(e)
                logging.error('执行update-sql语句失败')
                dbconnection.rollback()
                if i > 10:
                    break
                logging.error('执行insert-sql语句失败,重试中')
        dbconnection.commit()
        dbconnection.close()
