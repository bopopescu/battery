from .models import *
import datetime
from datetime import timezone
from datetime import timedelta
import datetime
import time
import logging

# 设置时区
TZ = 8


def get_current_scheme_interface(bid, cid):
    # 获取数据库中的测试方案数据
    if len(cellTestRealDataTable.objects.filter(boxID=bid, chnNum=cid)) == 0:
        logger = logging.getLogger("django")
        logger.error("当前通道无正在进行的测试")
        return {"schemeID": 0, "steps": []}
    tid = cellTestRealDataTable.objects.filter(boxID=bid, chnNum=cid)[0].testID
    if tid is None:
        return {"schemeID": 0, "steps": []}
    if len(testInfoTable.objects.filter(id=tid.id)) == 0:
        logger = logging.getLogger("django")
        logger.error("get_current_scheme_interface:err1")
        return {"schemeID": 0, "steps": []}
    sid = testInfoTable.objects.filter(id=tid.id)[0].planID
    steps = cellPlanDetailTable.objects.filter(planID=sid).order_by("step")
    step_list = []
    if len(steps) != 0:
        for j in steps:
            step = {
                "step": j.step,
                "LoadMode": j.mode,
                "U": float(j.u) / 1000,
                "I": float(j.i) / 1000,
                "t_LM": float(j.tTH) / 1000,
                "U_LM": float(j.uTH) / 1000,
                "I_LM": float(j.iTH) / 1000,
            }
            step_list.append(step)
    data = {
        "schemeID": int(sid.id),
        "steps": step_list
    }
    return data


def get_oven_status_interface():
    ovens = ovenDeviceTable.objects.all()
    data = []
    for i in ovens:
        oven = {
            "ID": i.ID,
            "curr": i.currState,
            "next": i.nextState,
            "PlanID": i.ovenPlanID.id if i.ovenPlanID is not None else None
        }
        bt0 = BigTestInfoTable.objects.filter(oven0ID=i.ID, completeFlag=0)
        bt1 = BigTestInfoTable.objects.filter(oven1ID=i.ID, completeFlag=0)
        bt2 = BigTestInfoTable.objects.filter(oven2ID=i.ID, completeFlag=0)
        bt3 = BigTestInfoTable.objects.filter(oven3ID=i.ID, completeFlag=0)
        bt = bt0 | bt1 | bt2 | bt3
        if len(bt) == 0:
            oven["T"] = -1
        else:
            crt = cellTestRealDataTable.objects.filter(bigTestID=bt[0])
            if len(crt) == 0:
                oven["T"] = -1
            else:
                oven["T"] = crt[0].Tc0 if len(bt0) != 0 \
                    else crt[0].Tc1 if len(bt1) != 0 \
                    else crt[0].Tc2 if len(bt2) != 0 else crt[0].Tc3
        data.append(oven)
    return {"oven": data}


def get_cells_info_interface():
    cells = cellDeviceTable.objects.all()
    data = []
    if len(cells) == 0:
        return {"cells": data}
    else:
        for c in cells:
            cell = {
                "cellID": c.cellID,
                "boxID": c.boxID.ID if c.boxID else None,
                "chnNum": c.chnNum,
                "oven0ID": c.mTc0ID.ID if c.mTc0ID else None,
                "oven1ID": c.mTc1ID.ID if c.mTc1ID else None,
                "oven2ID": c.mTc2ID.ID if c.mTc2ID else None,
                "oven3ID": c.mTc3ID.ID if c.mTc3ID else None,
                "H2ID": c.mH2ID.ID if c.mH2ID else None,
                "H2OID": c.mH2OID.ID if c.mH2OID else None,
                "N2ID": c.mN2ID.ID if c.mN2ID else None,
                "CO2ID": c.mCO2ID.ID if c.mCO2ID else None,
                "CH4ID": c.mCH4ID.ID if c.mCH4ID else None,
                "AIRID": c.mAIRID.ID if c.mAIRID else None,
                "wdjID": c.mTmID.ID if c.mTmID else None,
                "voltID": c.mVmID.ID if c.mVmID else None,
            }
            data.append(cell)
        return {"cells": data}


def get_tests_info_interface():
    bts = BigTestInfoTable.objects.all()
    data = []
    if len(bts) == 0:
        return {"tests": data}
    else:
        for bt in bts:
            sts = testInfoTable.objects.filter(bigTestID=bt)
            if len(sts) == 0:
                t = {
                    "BigTestID": bt.id,
                    "TestID": None,
                    "CellID": None,
                    "BoxID": None,
                    "ChnID": None,
                    "Oven0ID": bt.oven0ID.ID if bt.oven0ID else None,
                    "Oven1ID": bt.oven1ID.ID if bt.oven1ID else None,
                    "Oven2ID": bt.oven2ID.ID if bt.oven2ID else None,
                    "Oven3ID": bt.oven3ID.ID if bt.oven3ID else None,
                    "H2ID": bt.H2ID.ID if bt.H2ID else None,
                    "H2OID": bt.H2OID.ID if bt.H2OID else None,
                    "N2ID": bt.N2ID.ID if bt.N2ID else None,
                    "CO2ID": bt.CO2ID.ID if bt.CO2ID else None,
                    "CH4ID": bt.CH4ID.ID if bt.CH4ID else None,
                    "AIRID": bt.AIRID.ID if bt.AIRID else None,
                    "wdjID": bt.wdjID.ID if bt.wdjID else None,
                    "voltID": bt.voltID.ID if bt.voltID else None,
                    "StartTime": bt.startDate,
                    "EndTime": bt.endDate
                }
                data.append(t)
            else:
                for st in sts:
                    t = {
                        "BigTestID": bt.id,
                        "TestID": st.id,
                        "CellID": st.cellID.cellID if st.cellID else None,
                        "BoxID": st.boxID.ID if st.boxID else None,
                        "ChnID": st.chnNum,
                        "Oven0ID": bt.oven0ID.ID if bt.oven0ID else None,
                        "Oven1ID": bt.oven1ID.ID if bt.oven1ID else None,
                        "Oven2ID": bt.oven2ID.ID if bt.oven2ID else None,
                        "Oven3ID": bt.oven3ID.ID if bt.oven3ID else None,
                        "H2ID": bt.H2ID.ID if bt.H2ID else None,
                        "H2OID": bt.H2OID.ID if bt.H2OID else None,
                        "N2ID": bt.N2ID.ID if bt.N2ID else None,
                        "CO2ID": bt.CO2ID.ID if bt.CO2ID else None,
                        "CH4ID": bt.CH4ID.ID if bt.CH4ID else None,
                        "AIRID": bt.AIRID.ID if bt.AIRID else None,
                        "wdjID": bt.wdjID.ID if bt.wdjID else None,
                        "voltID": bt.voltID.ID if bt.voltID else None,
                        "StartTime": st.startDate,
                        "EndTime": st.endDate
                    }
                    data.append(t)
        return {"tests": data}


def get_old_oven_test_scheme_interface():
    # 获取数据库中的测试方案数据
    schemes = ovenPlanDetailTable.objects.values('ovenPlanID').distinct()
    scheme_num = len(schemes)
    scheme_list = []
    for i in schemes:
        step_list = []
        steps = ovenPlanDetailTable.objects.filter(ovenPlanID=i['ovenPlanID']).order_by('step')
        for j in steps:
            step = {
                "step": j.step,
                "T": j.T,
                "time": j.time,
            }
            step_list.append(step)
        scheme = {
            "id": i['ovenPlanID'],
            "name": ovenPlanTable.objects.filter(id=i['ovenPlanID']).values("name").distinct()[0]['name'],
            "steps": step_list
        }
        scheme_list.append(scheme)
    data = {
        "old_scheme_num": scheme_num,
        "old_scheme_list": scheme_list
    }
    return data


def get_old_test_scheme_interface():
    # 获取数据库中的测试方案数据
    schemes = cellPlanDetailTable.objects.values('planID').distinct()
    scheme_num = len(schemes)
    scheme_list = []
    for i in schemes:
        step_list = []
        steps = cellPlanDetailTable.objects.filter(planID=i['planID']).order_by('step')
        for j in steps:
            step = {
                "step": j.step,
                "LoadMode": j.mode,
                "U": float(j.u) / 1000 if j.u is not None else 0,
                "I": float(j.i) / 1000 if j.i is not None else 0,
                "t_LM": float(j.tTH) / 1000 if j.tTH is not None else 0,
                "U_LM": float(j.uTH) / 1000 if j.uTH is not None else 0,
                "I_LM": float(j.iTH) / 1000 if j.iTH is not None else 0,
            }
            step_list.append(step)
        scheme = {
            "id": i['planID'],
            "name": cellPlanTable.objects.filter(id=i['planID'])[0].name,
            "steps": step_list
        }
        scheme_list.append(scheme)
    data = {
        "old_scheme_num": scheme_num,
        "old_scheme_list": scheme_list
    }
    return data


def save_test_scheme_interface(new_scheme):
    # 传入参数为新的测试方案，存入数据库
    planid = cellPlanTable.objects.values("id")
    if len(planid) == 0:
        newid = 1
        planinfo = cellPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    else:
        maxid = planid.order_by("id").reverse()[0]['id']
        newid = maxid + 1
        planinfo = cellPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    steps = new_scheme['steps']
    flag = True
    for i in steps:
        try:
            step = cellPlanDetailTable()
            step.planID = planinfo
            step.step = 0 if i['step'] is None else int(i['step'])
            step.mode = "" if i['LoadMode'] is None else i['LoadMode']
            step.i = 0 if i['I'] is None else int(float(i['I']) * 1000)
            step.u = 0 if i['U'] is None else int(float(i['U']) * 1000)
            step.iTH = 0 if i['I_LM'] is None else int(float(i['I_LM']) * 1000)
            step.uTH = 0 if i['U_LM'] is None else int(float(i['U_LM']) * 1000)
            step.tTH = 0 if i['t_LM'] is None else int(float(i['t_LM']) * 1000)
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error("保存电子负载方案过程中出错")
            logger.error(str(e))
            flag = False
            break
        step.save()

    return flag


def save_oven_test_scheme_interface(new_scheme):
    # 传入参数为新的测试方案，存入数据库
    planid = ovenPlanTable.objects.values("id")
    if len(planid) == 0:
        newid = 1
        planinfo = ovenPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    else:
        maxid = planid.order_by("id").reverse()[0]['id']
        newid = maxid + 1
        planinfo = ovenPlanTable.objects.create(id=newid, name=new_scheme['name'], steps=len(new_scheme['steps']))
    steps = new_scheme['steps']
    flag = True
    for i in steps:
        try:
            step = ovenPlanDetailTable()
            step.ovenPlanID = planinfo
            step.step = 0 if i['step'] is None else int(i['step'])
            step.T = 0 if i['T'] is None else int(i['T'])
            step.time = 0 if i['time'] is None else int(i['time'])
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error("保存电炉方案过程中出错")
            logger.error(str(e))
            flag = False
            break
        step.save()

    return flag


def delete_test_scheme_interface(schemeID):
    return


def get_box_info_interface():
    # 给出所有接着电池的箱号以及对应通道号
    box_list = []
    oven_list = []
    boxes = cellDeviceTable.objects.values('boxID').distinct()
    if len(boxes) == 0:
        logger = logging.getLogger("django")
        logger.error("没有任何箱号")
    #        return {"box": box_list}
    else:
        for i in boxes:
            bid = i['boxID']
            channels = cellDeviceTable.objects.filter(boxID=bid).values('chnNum').distinct()
            channel_list = []
            for j in channels:
                channel_list.append(j['chnNum'])
            box = {
                "id": bid,
                "channel": channel_list
            }
            box_list.append(box)
    ovens = ovenDeviceTable.objects.all()
    if len(ovens) == 0:
        logger = logging.getLogger("django")
        logger.error("没有任何电炉")
    else:
        for i in ovens:
            oven = {"id": i.ID}
            oven_list.append(oven)
    data = {"box": box_list, "oven": oven_list}
    return data


def get_real_time_test_data_interface(box_id, cha_id):
    # 获取给定通道的实时数据
    # 首先获取该通道的最近测试ID
    test_id = get_latest_testid_interface(box_id, cha_id)
    data = {
        'I': {}, 'U': {},
        'Q_N2': {}, 'Q_H2': {}, 'Q_CO2': {}, 'Q_CH4': {}, 'Q_Air': {}, 'Q_H2O': {},
        'Tc0': {}, 'Tc1': {}, 'Tc2': {}, 'Tc3': {},
        'Tm0': {}, 'Tm1': {}, 'Tm2': {}, 'Tm3': {}, 'Tm4': {}, 'Tm5': {}, 'Tm6': {}, 'Tm7': {}, 'Tm8': {}, 'Tm9': {},
        'Tm10': {}, 'Tm11': {}, 'Tm12': {}, 'Tm13': {}, 'Tm14': {}, 'Tm15': {}, 'Tm16': {}, 'Tm17': {}, 'Tm18': {},
        'Tm19': {},
        'Vm0': {}, 'Vm1': {}, 'Vm2': {}, 'Vm3': {}, 'Vm4': {}, 'Vm5': {}, 'Vm6': {}, 'Vm7': {}, 'Vm8': {}, 'Vm9': {},
        'Vm10': {}, 'Vm11': {}, 'Vm12': {}, 'Vm13': {}, 'Vm14': {}, 'Vm15': {}, 'Vm16': {}, 'Vm17': {}, 'Vm18': {},
        'Vm19': {},
    }
    if test_id == -1:
        return data
    try:
        rt_data = cellTestRealDataTable.objects.get(testID=test_id)  # 数据的时间戳是秒级，而js默认是ms级，因此需要*1000
    except:
        logger = logging.getLogger("django")
        logger.error("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在实时数据")
        return data

    data = {
        'I': {"name": int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
              "value": [int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                        float(rt_data.i) / 1000]},
        'U': {"name": int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
              "value": [int(rt_data.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                        float(rt_data.u) / 1000]},
        'Q_N2': {"name": int(rt_data.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                 "value": [int(rt_data.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           rt_data.qN2]},
        'Q_H2': {"name": int(rt_data.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                 "value": [int(rt_data.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           rt_data.qH2]},
        'Q_CO2': {"name": int(rt_data.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qCO2]},
        'Q_CH4': {"name": int(rt_data.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qCH4]},
        'Q_Air': {"name": int(rt_data.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qAIR]},
        'Q_H2O': {"name": int(rt_data.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                  "value": [int(rt_data.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                            rt_data.qH2O]},
        'Tc0': {"name": int(rt_data.tTc0.timestamp() * 1000),
                "value": [int(rt_data.tTc0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tc0)]},
        'Tc1': {"name": int(rt_data.tTc1.timestamp() * 1000),
                "value": [int(rt_data.tTc1.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tc1)]},
        'Tc2': {"name": int(rt_data.tTc2.timestamp() * 1000),
                "value": [int(rt_data.tTc2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tc2)]},
        'Tc3': {"name": int(rt_data.tTc3.timestamp() * 1000),
                "value": [int(rt_data.tTc3.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tc3)]},
        'Tm0': {"name": int(rt_data.tTm0.timestamp() * 1000),
                "value": [int(rt_data.tTm0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm0)]},
        'Tm1': {"name": int(rt_data.tTm1.timestamp() * 1000),
                "value": [int(rt_data.tTm1.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm1)]},
        'Tm2': {"name": int(rt_data.tTm2.timestamp() * 1000),
                "value": [int(rt_data.tTm2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm2)]},
        'Tm3': {"name": int(rt_data.tTm3.timestamp() * 1000),
                "value": [int(rt_data.tTm3.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm3)]},
        'Tm4': {"name": int(rt_data.tTm4.timestamp() * 1000),
                "value": [int(rt_data.tTm4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm4)]},
        'Tm5': {"name": int(rt_data.tTm5.timestamp() * 1000),
                "value": [int(rt_data.tTm5.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm5)]},
        'Tm6': {"name": int(rt_data.tTm6.timestamp() * 1000),
                "value": [int(rt_data.tTm6.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm6)]},
        'Tm7': {"name": int(rt_data.tTm7.timestamp() * 1000),
                "value": [int(rt_data.tTm7.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm7)]},
        'Tm8': {"name": int(rt_data.tTm8.timestamp() * 1000),
                "value": [int(rt_data.tTm8.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm8)]},
        'Tm9': {"name": int(rt_data.tTm9.timestamp() * 1000),
                "value": [int(rt_data.tTm9.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                          float(rt_data.Tm9)]},
        'Tm10': {"name": int(rt_data.tTm10.timestamp() * 1000),
                 "value": [int(rt_data.tTm10.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm10)]},
        'Tm11': {"name": int(rt_data.tTm11.timestamp() * 1000),
                 "value": [int(rt_data.tTm11.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm11)]},
        'Tm12': {"name": int(rt_data.tTm12.timestamp() * 1000),
                 "value": [int(rt_data.tTm12.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm12)]},
        'Tm13': {"name": int(rt_data.tTm13.timestamp() * 1000),
                 "value": [int(rt_data.tTm13.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm13)]},
        'Tm14': {"name": int(rt_data.tTm14.timestamp() * 1000),
                 "value": [int(rt_data.tTm14.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm14)]},
        'Tm15': {"name": int(rt_data.tTm15.timestamp() * 1000),
                 "value": [int(rt_data.tTm15.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm15)]},
        'Tm16': {"name": int(rt_data.tTm16.timestamp() * 1000),
                 "value": [int(rt_data.tTm16.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm16)]},
        'Tm17': {"name": int(rt_data.tTm17.timestamp() * 1000),
                 "value": [int(rt_data.tTm17.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm17)]},
        'Tm18': {"name": int(rt_data.tTm18.timestamp() * 1000),
                 "value": [int(rt_data.tTm18.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm18)]},
        'Tm19': {"name": int(rt_data.tTm19.timestamp() * 1000),
                 "value": [int(rt_data.tTm19.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
                           float(rt_data.Tm19)]},
    }
    return data


def get_history_test_data_interface(box_id, cha_id, test_id):
    # 获取给定通道，给定测试id的历史数据
    ## bug:数据必须按照时间顺序排列 否则显示会有问题
    hs_data = cellTestHistoryDataTable.objects.filter(testID=test_id).order_by("celldata_time")
    data = {
        'I': [], 'U': [],
        'Q_N2': [], 'Q_H2': [], 'Q_CO2': [], 'Q_CH4': [], 'Q_Air': [], 'Q_H2O': [],
        'Tc0': [], 'Tc1': [], 'Tc2': [], 'Tc3': [],
        'Tm0': [], 'Tm1': [], 'Tm2': [], 'Tm3': [], 'Tm4': [], 'Tm5': [], 'Tm6': [], 'Tm7': [], 'Tm8': [], 'Tm9': [],
        'Tm10': [], 'Tm11': [], 'Tm12': [], 'Tm13': [], 'Tm14': [], 'Tm15': [], 'Tm16': [], 'Tm17': [], 'Tm18': [],
        'Tm19': [],
        'Vm0': [], 'Vm1': [], 'Vm2': [], 'Vm3': [], 'Vm4': [], 'Vm5': [], 'Vm6': [], 'Vm7': [], 'Vm8': [], 'Vm9': [],
        'Vm10': [], 'Vm11': [], 'Vm12': [], 'Vm13': [], 'Vm14': [], 'Vm15': [], 'Vm16': [], 'Vm17': [], 'Vm18': [],
        'Vm19': [],
    }
    if len(hs_data) == 0:
        logger = logging.getLogger("django")
        logger.error("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在历史数据")
        return data

    timeformat = lambda x: int(x.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000)
    for i in hs_data:
        data['I'].append({
            "name": timeformat(i.celldata_time), "value": [timeformat(i.celldata_time), float(i.i) / 1000]})
        data['U'].append({
            "name": timeformat(i.celldata_time), "value": [timeformat(i.celldata_time), float(i.u) / 1000]})
        data['Q_N2'].append({"name": timeformat(i.tN2), "value": [timeformat(i.tN2), i.qN2]})
        data['Q_H2'].append({"name": timeformat(i.tH2), "value": [timeformat(i.tN2), i.qH2]})
        data['Q_H2O'].append({"name": timeformat(i.tH2O), "value": [timeformat(i.tH2O), i.qH2O]})
        data['Q_CO2'].append({"name": timeformat(i.tCO2), "value": [timeformat(i.tCO2), i.qCO2]})
        data['Q_Air'].append({"name": timeformat(i.tAIR), "value": [timeformat(i.tAIR), i.qAIR]})
        data['Q_CH4'].append({"name": timeformat(i.tCH4), "value": [timeformat(i.tCH4), i.qCH4]})
        data['Tc0'].append({"name": timeformat(i.tTc0), "value": [timeformat(i.tTc0), i.Tc0]})
        data['Tc1'].append({"name": timeformat(i.tTc1), "value": [timeformat(i.tTc1), i.Tc1]})
        data['Tc2'].append({"name": timeformat(i.tTc2), "value": [timeformat(i.tTc2), i.Tc2]})
        data['Tc3'].append({"name": timeformat(i.tTc3), "value": [timeformat(i.tTc3), i.Tc3]})
        data['Tm0'].append({"name": timeformat(i.tTm0), "value": [timeformat(i.tTm0), i.Tm0]})
        data['Tm1'].append({"name": timeformat(i.tTm1), "value": [timeformat(i.tTm1), i.Tm1]})
        data['Tm2'].append({"name": timeformat(i.tTm2), "value": [timeformat(i.tTm2), i.Tm2]})
        data['Tm3'].append({"name": timeformat(i.tTm3), "value": [timeformat(i.tTm3), i.Tm3]})
        data['Tm4'].append({"name": timeformat(i.tTm4), "value": [timeformat(i.tTm4), i.Tm4]})
        data['Tm5'].append({"name": timeformat(i.tTm5), "value": [timeformat(i.tTm5), i.Tm5]})
        data['Tm6'].append({"name": timeformat(i.tTm6), "value": [timeformat(i.tTm6), i.Tm6]})
        data['Tm7'].append({"name": timeformat(i.tTm7), "value": [timeformat(i.tTm7), i.Tm7]})
        data['Tm8'].append({"name": timeformat(i.tTm8), "value": [timeformat(i.tTm8), i.Tm8]})
        data['Tm9'].append({"name": timeformat(i.tTm9), "value": [timeformat(i.tTm9), i.Tm9]})
        data['Tm10'].append({"name": timeformat(i.tTm10), "value": [timeformat(i.tTm10), i.Tm10]})
        data['Tm11'].append({"name": timeformat(i.tTm11), "value": [timeformat(i.tTm11), i.Tm11]})
        data['Tm12'].append({"name": timeformat(i.tTm12), "value": [timeformat(i.tTm12), i.Tm12]})
        data['Tm13'].append({"name": timeformat(i.tTm13), "value": [timeformat(i.tTm13), i.Tm13]})
        data['Tm14'].append({"name": timeformat(i.tTm14), "value": [timeformat(i.tTm14), i.Tm14]})
        data['Tm15'].append({"name": timeformat(i.tTm15), "value": [timeformat(i.tTm15), i.Tm15]})
        data['Tm16'].append({"name": timeformat(i.tTm16), "value": [timeformat(i.tTm16), i.Tm16]})
        data['Tm17'].append({"name": timeformat(i.tTm17), "value": [timeformat(i.tTm17), i.Tm17]})
        data['Tm18'].append({"name": timeformat(i.tTm18), "value": [timeformat(i.tTm18), i.Tm18]})
        data['Tm19'].append({"name": timeformat(i.tTm19), "value": [timeformat(i.tTm19), i.Tm19]})
        data['Vm0'].append({"name": timeformat(i.tVm0), "value": [timeformat(i.tVm0), i.Vm0]})
        data['Vm1'].append({"name": timeformat(i.tVm1), "value": [timeformat(i.tVm1), i.Vm1]})
        data['Vm2'].append({"name": timeformat(i.tVm2), "value": [timeformat(i.tVm2), i.Vm2]})
        data['Vm3'].append({"name": timeformat(i.tVm3), "value": [timeformat(i.tVm3), i.Vm3]})
        data['Vm4'].append({"name": timeformat(i.tVm4), "value": [timeformat(i.tVm4), i.Vm4]})
        data['Vm5'].append({"name": timeformat(i.tVm5), "value": [timeformat(i.tVm5), i.Vm5]})
        data['Vm6'].append({"name": timeformat(i.tVm6), "value": [timeformat(i.tVm6), i.Vm6]})
        data['Vm7'].append({"name": timeformat(i.tVm7), "value": [timeformat(i.tVm7), i.Vm7]})
        data['Vm8'].append({"name": timeformat(i.tVm8), "value": [timeformat(i.tVm8), i.Vm8]})
        data['Vm9'].append({"name": timeformat(i.tVm9), "value": [timeformat(i.tVm9), i.Vm9]})
        data['Vm10'].append({"name": timeformat(i.tVm10), "value": [timeformat(i.tVm10), i.Vm10]})
        data['Vm11'].append({"name": timeformat(i.tVm11), "value": [timeformat(i.tVm11), i.Vm11]})
        data['Vm12'].append({"name": timeformat(i.tVm12), "value": [timeformat(i.tVm12), i.Vm12]})
        data['Vm13'].append({"name": timeformat(i.tVm13), "value": [timeformat(i.tVm13), i.Vm13]})
        data['Vm14'].append({"name": timeformat(i.tVm14), "value": [timeformat(i.tVm14), i.Vm14]})
        data['Vm15'].append({"name": timeformat(i.tVm15), "value": [timeformat(i.tVm15), i.Vm15]})
        data['Vm16'].append({"name": timeformat(i.tVm16), "value": [timeformat(i.tVm16), i.Vm16]})
        data['Vm17'].append({"name": timeformat(i.tVm17), "value": [timeformat(i.tVm17), i.Vm17]})
        data['Vm18'].append({"name": timeformat(i.tVm18), "value": [timeformat(i.tVm18), i.Vm18]})
        data['Vm19'].append({"name": timeformat(i.tVm19), "value": [timeformat(i.tVm19), i.Vm19]})

        # data['I'].append({
        #     "name": int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #               float(i.i) / 1000]})
        # data['U'].append({
        #     "name": int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.celldata_time.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #               float(i.u) / 1000]})
        # data['Q_N2'].append({
        #     "name": int(i.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tN2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qN2]})
        # data['Q_H2'].append({
        #     "name": int(i.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tH2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qH2]})
        # data['Q_CO2'].append({
        #     "name": int(i.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tCO2.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qCO2]})
        # data['Q_CH4'].append({
        #     "name": int(i.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tCH4.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qCH4]})
        # data['Q_Air'].append({
        #     "name": int(i.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tAIR.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qAIR]})
        # data['Q_H2O'].append({
        #     "name": int(i.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tH2O.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), i.qH2O]})
        # data['Tc0'].append({
        #     "name": int(i.tTc0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000),
        #     "value": [int(i.tTc0.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000), float(i.T0)]})
    return data


def get_real_time_info_interface(box_id, cha_id):
    test_id = get_latest_testid_interface(box_id, cha_id)
    data = {
        "I": 0, "U": 0, "q": 0, "k": 0,
        "Tc0": 0, "Tc1": 0, "Tc2": 0, "Tc3": 0,
        "Tm0": 0, "Tm1": 0, "Tm2": 0, "Tm3": 0, "Tm4": 0, "Tm5": 0, "Tm6": 0, "Tm7": 0, "Tm8": 0, "Tm9": 0,
        "Tm10": 0, "Tm11": 0, "Tm12": 0, "Tm13": 0, "Tm14": 0, "Tm15": 0, "Tm16": 0, "Tm17": 0, "Tm18": 0, "Tm19": 0,
        "Vm0": 0, "Vm1": 0, "Vm2": 0, "Vm3": 0, "Vm4": 0, "Vm5": 0, "Vm6": 0, "Vm7": 0, "Vm8": 0, "Vm9": 0,
        "Vm10": 0, "Vm11": 0, "Vm12": 0, "Vm13": 0, "Vm14": 0, "Vm15": 0, "Vm16": 0, "Vm17": 0, "Vm18": 0, "Vm19": 0,
        "Q_H2": 0, "Q_CO2": 0, "Q_N2": 0, "Q_CH4": 0, "Q_Air": 0, "Q_H2O": 0,

    }
    if test_id == -1:
        return data
    try:
        rt_data = cellTestRealDataTable.objects.get(testID=test_id)  # 数据的时间戳是秒级，而js默认是ms级，因此需要*1000
    except:
        logger = logging.getLogger("django")
        logger.error("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "  testID:" + str(test_id) + "    不存在实时信息")
        return data
    dataformat = lambda x: float(x) if x is not None else 0
    data['I'] = float(rt_data.i) / 1000 if rt_data.i is not None else 0
    data['U'] = float(rt_data.u) / 1000 if rt_data.u is not None else 0
    data['q'] = float(rt_data.q) if rt_data.q is not None else 0
    data['k'] = rt_data.n if rt_data.n is not None else 0
    data['Tc0'] = dataformat(rt_data.Tc0)
    data['Tc1'] = dataformat(rt_data.Tc1)
    data['Tc2'] = dataformat(rt_data.Tc2)
    data['Tc3'] = dataformat(rt_data.Tc3)
    data['Q_N2'] = dataformat(rt_data.qN2)
    data['Q_H2'] = dataformat(rt_data.qH2)
    data['Q_CO2'] = dataformat(rt_data.qCO2)
    data['Q_CH4'] = dataformat(rt_data.qCH4)
    data['Q_Air'] = dataformat(rt_data.qAIR)
    data['Q_H2O'] = dataformat(rt_data.qH2O)
    data['Tm0'] = dataformat(rt_data.Tm0)
    data['Tm1'] = dataformat(rt_data.Tm1)
    data['Tm2'] = dataformat(rt_data.Tm2)
    data['Tm3'] = dataformat(rt_data.Tm3)
    data['Tm4'] = dataformat(rt_data.Tm4)
    data['Tm5'] = dataformat(rt_data.Tm5)
    data['Tm6'] = dataformat(rt_data.Tm6)
    data['Tm7'] = dataformat(rt_data.Tm7)
    data['Tm8'] = dataformat(rt_data.Tm8)
    data['Tm9'] = dataformat(rt_data.Tm9)
    data['Tm10'] = dataformat(rt_data.Tm10)
    data['Tm11'] = dataformat(rt_data.Tm11)
    data['Tm12'] = dataformat(rt_data.Tm12)
    data['Tm13'] = dataformat(rt_data.Tm13)
    data['Tm14'] = dataformat(rt_data.Tm14)
    data['Tm15'] = dataformat(rt_data.Tm15)
    data['Tm16'] = dataformat(rt_data.Tm16)
    data['Tm17'] = dataformat(rt_data.Tm17)
    data['Tm18'] = dataformat(rt_data.Tm18)
    data['Tm19'] = dataformat(rt_data.Tm19)
    data['Vm0'] = dataformat(rt_data.Vm0)
    data['Vm1'] = dataformat(rt_data.Vm1)
    data['Vm2'] = dataformat(rt_data.Vm2)
    data['Vm3'] = dataformat(rt_data.Vm3)
    data['Vm4'] = dataformat(rt_data.Vm4)
    data['Vm5'] = dataformat(rt_data.Vm5)
    data['Vm6'] = dataformat(rt_data.Vm6)
    data['Vm7'] = dataformat(rt_data.Vm7)
    data['Vm8'] = dataformat(rt_data.Vm8)
    data['Vm9'] = dataformat(rt_data.Vm9)
    data['Vm10'] = dataformat(rt_data.Vm10)
    data['Vm11'] = dataformat(rt_data.Vm11)
    data['Vm12'] = dataformat(rt_data.Vm12)
    data['Vm13'] = dataformat(rt_data.Vm13)
    data['Vm14'] = dataformat(rt_data.Vm14)
    data['Vm15'] = dataformat(rt_data.Vm15)
    data['Vm16'] = dataformat(rt_data.Vm16)
    data['Vm17'] = dataformat(rt_data.Vm17)
    data['Vm18'] = dataformat(rt_data.Vm18)
    data['Vm19'] = dataformat(rt_data.Vm19)
    return data


def get_latest_testid_interface(box_id, cha_id):
    # 获取给定通道的当前测试id
    # 假定最近的id存在最后面，即test_id只会递增
    try:
        test_id = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('id').reverse()[0].id
    except:
        logger = logging.getLogger("django")
        logger.error("boxID:" + str(box_id) + "  chaID:" + str(cha_id) + "    还没有进行过测试")
        return -1
    return test_id


def get_schemeid_interface(box_id, cha_id, test_id):
    # 获取给定测试的测试id
    pass


def start_channel_interface(box_id, cha_id, scheme_id):
    # cellid = cellDeviceTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('cellID').reverse()
    cellid = cellTestRealDataTable.objects.filter(boxID=box_id, chnNum=cha_id)
    if len(cellid) == 0:
        logger = logging.getLogger("django")
        logger.error("startchannel:当前通道还未创建realdatatable")
        return "启动失败：当前通道还未启动电炉"
    cellid = cellid[0].cellID
    bigtest = BigTestInfoTable.objects.filter(cellID=cellid, boxID=box_id, chnNum=cha_id, completeFlag=0).order_by(
        "startDate").reverse()
    if len(bigtest) == 0:
        logger = logging.getLogger("django")
        logger.error("startchannel:当前通道还未创建bigtest")
        return "启动失败：当前通道还未启动电炉"
    bigtest = bigtest[0]
    try:
        planid = cellPlanTable.objects.get(id=scheme_id)
    except:
        logger = logging.getLogger("django")
        logger.error("启动失败：找不到电子负载测试方案")
        return "启动失败：找不到该测试方案"
    try:
        box_id = boxDeviceTable.objects.get(ID=box_id)
    except:
        logger = logging.getLogger("django")
        logger.error("启动失败：找不到电子负载箱号")
        return "启动失败：找不到该负载箱号"
    testid = testInfoTable(boxID=box_id, chnNum=cha_id, bigTestID=bigtest, planID=planid, cellID=cellid, completeFlag=0,
                           startDate=datetime.datetime.now())
    testid.save()
    steps = cellPlanDetailTable.objects.filter(id=scheme_id).order_by('step')
    x = cellTestRealDataTable.objects.filter(cellID=cellid, boxID=box_id, chnNum=cha_id, currState="stop",
                                             nextState="stop")
    if len(x) == 0:
        logger = logging.getLogger("django")
        logger.error("启动失败：未创建realdatatable")
        testid.delete()
        return "启动失败：当前通道还未启动电炉"
    elif len(x) > 1:
        logger = logging.getLogger("django")
        logger.warning("启动通道：多条realdatatable")
        x.update(cellID=cellid, boxID=box_id, chnNum=cha_id, testID=testid, totalStepN=len(steps), currState="stop",
                 nextState="start")
        return "启动成功"
    else:
        x.update(boxID=box_id, chnNum=cha_id, testID=testid, totalStepN=len(steps), currState="stop", nextState="start")
        return "启动成功"


def stop_channel_interface(box_id, cha_id):
    tid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(tid) == 0:
        logger = logging.getLogger("django")
        logger.error("停止失败：未查询到该通道的testID")
        return "停止失败"
    crt = cellTestRealDataTable.objects.filter(boxID=box_id, chnNum=cha_id, testID=tid[0], bigTestID=tid[0].bigTestID)
    if len(crt) == 0:
        logger = logging.getLogger("django")
        logger.error("停止失败：还未创建realdatatable")
        return "停止失败"
    elif len(crt) > 1:
        logger = logging.getLogger("django")
        logger.error("停止失败：多个realdatatable")
        return "停止失败"
    if crt[0].currState == "stop":
        logger = logging.getLogger("django")
        logger.warning("停止通道：已经停止")
        if crt[0].testID is not None:
            testInfoTable.objects.filter(id=crt[0].testID.id).update(completeFlag=1, endDate=datetime.datetime.now())
            crt.update(nextState="stop", testID=None)
        return "已经停止"
    if crt[0].nextState == "stop":
        logger = logging.getLogger("django")
        logger.warning("停止通道：正尝试停止")
        return "正在尝试停止......"

    if crt[0].testID is not None:
        testInfoTable.objects.filter(id=crt[0].testID.id).update(completeFlag=1, endDate=datetime.datetime.now())
        crt.update(nextState="stop", testID=None)
    return "停止成功"

    # testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id)
    # if len(testid) == 0:
    #     print("stopchannel:testid not found")
    #     return False
    # elif len(testid) > 1:
    #     print("stopchannel:当前通道有多条测试记录，选取最后一条")
    # testid = testid.order_by("id").reverse()[0]
    # rows = cellTestRealDataTable.objects.filter(testID=testid).update(nextState="stop")
    # testid.completeFlag = 1
    # testid.endDate = datetime.datetime.now()
    # return rows


def pause_channel_interface(box_id, cha_id):
    testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(testid) == 0:
        logger = logging.getLogger("django")
        logger.error("暂停失败：没找到testid")
        return "暂停失败"
    elif len(testid) > 1:
        logger = logging.getLogger("django")
        logger.warning("暂停通道：多条testid")
    testid = testid.order_by("id").reverse()[0]
    rows = cellTestRealDataTable.objects.filter(testID=testid, currState="start").update(nextState="pause")
    return "暂停成功"


def continue_channel_interface(box_id, cha_id):
    testid = testInfoTable.objects.filter(boxID=box_id, chnNum=cha_id, completeFlag=0)
    if len(testid) == 0:
        logger = logging.getLogger("django")
        logger.error("继续失败：没找到testid")
        return "继续通道失败"
    elif len(testid) > 1:
        logger = logging.getLogger("django")
        logger.warning("继续通道：多条testid")
    testid = testid.order_by("id").reverse()[0]
    rows = cellTestRealDataTable.objects.filter(testID=testid, currState="pause").update(nextState="resume")
    return "继续通道成功"


# def make_test_interface(box_id, cha_id, scheme_id, oven_scheme_id):
#     # 创建父测试
#     cellid = cellDeviceTable.objects.filter(boxID=box_id, chnNum=cha_id).order_by('cellID').reverse()[0]
#     planid = planInfoTable.objects.get(id=scheme_id)
#     oplanid = ovenPlanInfoTable.objects.get(id=oven_scheme_id)
#     testid = testInfoTable(boxID=box_id, chnNum=cha_id, planID=planid, cellID=cellid)
#     testid.save()
#     steps = planTable.objects.filter(planID=scheme_id).order_by('step')
#     x = cellRealDataTable.objects.filter(cellID=cellid)
#     if len(x) == 0:
#         crd = cellRealDataTable(cellID=cellid, boxID=box_id, chnNum=cha_id, testID=testid, planID=planid,
#                                 totalStepN=len(steps), currState="stop", nextState="stop", ovenPlanID=oplanid,
#                                 currOvenState="stop", nextOvenState="stop")
#         crd.save()
#     elif len(x) > 1:
#         print("不止一条测试")
#         x.update(boxID=box_id, chnNum=cha_id, ovenPlanID=oplanid, currOvenState="stop", nextOvenState="stop")
#     else:
#         x.update(boxID=box_id, chnNum=cha_id, ovenPlanID=oplanid, currOvenState="stop", nextOvenState="stop")


def start_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    # 创建父测试
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        logger = logging.getLogger("django")
        logger.error("启动电炉失败：没有该电炉")
        return "启动电炉失败：没有该电炉"
    if ovenid.currState == "start":
        logger = logging.getLogger("django")
        logger.error("启动电炉失败：该电炉已启动")
        return "启动电炉失败：该电炉已启动"
    if ovenid.nextState == "start":
        logger = logging.getLogger("django")
        logger.error("启动电炉失败：正在尝试启动")
        return "启动电炉失败：正在尝试启动"
    try:
        ovenplanid = ovenPlanTable.objects.get(id=oven_scheme_id)
    except:
        logger = logging.getLogger("django")
        logger.error("启动电炉失败：没有该测试方案")
        return "启动电炉失败：没有该测试方案"
    cell1 = cellDeviceTable.objects.filter(mTc0ID=ovenid)
    cell2 = cellDeviceTable.objects.filter(mTc1ID=ovenid)
    cell3 = cellDeviceTable.objects.filter(mTc2ID=ovenid)
    cell4 = cellDeviceTable.objects.filter(mTc3ID=ovenid)
    cell = cell1 | cell2 | cell3 | cell4
    if len(cell) == 0:
        logger = logging.getLogger("django")
        logger.warning("启动电炉：该电炉里面没有电池")
        bt = BigTestInfoTable(oven0ID=ovenid, ovenPlanID=ovenplanid, completeFlag=0)
        bt.save()
        crt = cellTestRealDataTable.objects.filter(bigTestID=None, boxID=None, chnNum=None)
        if len(crt) == 0:
            crt = cellTestRealDataTable(bigTestID=bt, currState="stop", nextState="stop")
            crt.save()
        else:
            crt.update(bigTestID=bt, currState="stop", nextState="stop")
        # return "启动成功！警告：该电炉中没有电池"
    for i in cell:
        bt = BigTestInfoTable.objects.filter(cellID=i, completeFlag=0)
        if len(bt) != 0:
            if len(cell1) != 0:
                bt.update(oven0ID=ovenid)
            elif len(cell2) != 0:
                bt.update(oven1ID=ovenid)
            elif len(cell3) != 0:
                bt.update(oven2ID=ovenid)
            elif len(cell4) != 0:
                bt.update(oven3ID=ovenid)
        else:
            if len(cell1) != 0:
                bt = BigTestInfoTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, H2ID=i.mH2ID, N2ID=i.mN2ID,
                                      CO2ID=i.mCO2ID, CH4ID=i.mCH4ID, AIRID=i.mAIRID, H2OID=i.mH2OID, oven0ID=ovenid,
                                      wdjID=i.mTmID, voltID=i.mVmID, completeFlag=0)
            elif len(cell2) != 0:
                bt = BigTestInfoTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, H2ID=i.mH2ID, N2ID=i.mN2ID,
                                      CO2ID=i.mCO2ID, CH4ID=i.mCH4ID, AIRID=i.mAIRID, H2OID=i.mH2OID, oven1ID=ovenid,
                                      wdjID=i.mTmID, voltID=i.mVmID, completeFlag=0)
            elif len(cell3) != 0:
                bt = BigTestInfoTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, H2ID=i.mH2ID, N2ID=i.mN2ID,
                                      CO2ID=i.mCO2ID, CH4ID=i.mCH4ID, AIRID=i.mAIRID, H2OID=i.mH2OID, oven2ID=ovenid,
                                      wdjID=i.mTmID, voltID=i.mVmID, completeFlag=0)
            elif len(cell4) != 0:
                bt = BigTestInfoTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, H2ID=i.mH2ID, N2ID=i.mN2ID,
                                      CO2ID=i.mCO2ID, CH4ID=i.mCH4ID, AIRID=i.mAIRID, H2OID=i.mH2OID, oven3ID=ovenid,
                                      wdjID=i.mTmID, voltID=i.mVmID, completeFlag=0)

            bt.save()
            crt = cellTestRealDataTable.objects.filter(boxID=i.boxID, chnNum=i.chnNum)
            if len(crt) == 0:
                crt = cellTestRealDataTable(cellID=i, boxID=i.boxID, chnNum=i.chnNum, bigTestID=bt, currState="stop",
                                            nextState="stop")
                crt.save()
            else:
                crt.update(cellID=i, bigTestID=bt, currState="stop", nextState="stop")
    ovenDeviceTable.objects.filter(ID=oven_id, currState="stop").update(ovenPlanID=ovenplanid, nextState="start")
    logger = logging.getLogger("django")
    logger.info("启动电炉：成功")
    return "启动电炉成功"


# todo
def stop_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        logger = logging.getLogger("django")
        logger.error("停止电炉失败：没有该电炉")
        return "停止电炉失败：没有该电炉"
    if ovenid.currState == "stop" and ovenid.nextState == "stop":
        logger = logging.getLogger("django")
        logger.error("停止电炉失败：该电炉已停止")
        return "停止电炉失败：该电炉已停止"
    if ovenid.nextState == "stop":
        logger = logging.getLogger("django")
        logger.error("停止电炉失败：该电炉正尝试停止")
        return "正尝试停止......"

    bt0 = BigTestInfoTable.objects.filter(oven0ID=ovenid, completeFlag=0)
    bt1 = BigTestInfoTable.objects.filter(oven1ID=ovenid, completeFlag=0)
    bt2 = BigTestInfoTable.objects.filter(oven2ID=ovenid, completeFlag=0)
    bt3 = BigTestInfoTable.objects.filter(oven3ID=ovenid, completeFlag=0)
    bt = bt0 | bt1 | bt2 | bt3
    if len(bt) == 1 and bt[0].cellID is None:
        cellTestRealDataTable.objects.get(bigTestID=bt[0]).delete()
        ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="stop")
        bt.update(completeFlag=1, endDate=datetime.datetime.now())
        logger = logging.getLogger("django")
        logger.info("停止电炉:成功")
        return "停止电炉成功！"
    if len(bt) == 1 and len(testInfoTable.objects.filter(bigTestID__in=bt, completeFlag=0)) != 0:
        logger = logging.getLogger("django")
        logger.error("停止电炉失败：该父测试下还有未完成的子测试，结束失败")
        return "停止电炉失败：该电炉内部还有电池正在测试！"
    # todo
    count=0
    if bt[0].oven0ID is not None and bt[0].oven0ID.nextState == "start":
        count=count+1
    if bt[0].oven1ID is not None and bt[0].oven1ID.nextState == "start":
        count=count+1
    if bt[0].oven2ID is not None and bt[0].oven2ID.nextState == "start":
        count=count+1
    if bt[0].oven3ID is not None and bt[0].oven3ID.nextState == "start":
        count=count+1
    if count > 1:
        ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="stop")
        logger = logging.getLogger("django")
        logger.info("停止电炉:成功,但对应父测试未结束，因为还有其他电炉")
        return "停止电炉成功，但对应父测试未结束，因为还有其他电炉正在运行！"
    else:
        if len(testInfoTable.objects.filter(bigTestID__in=bt, completeFlag=0)) != 0:
            logger = logging.getLogger("django")
            logger.error("停止电炉失败：该父测试下还有未完成的子测试，结束失败")
            return "停止电炉失败：该电炉内部还有电池正在测试！"
        else:
            cellTestRealDataTable.objects.filter(bigTestID__in=bt).delete()
            ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="stop")
            bt.update(completeFlag=1, endDate=datetime.datetime.now())
            logger = logging.getLogger("django")
            logger.info("停止电炉:成功")
            return "停止电炉成功！"




def pause_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        logger = logging.getLogger("django")
        logger.error("暂停电炉失败：没有该电炉")
        return "暂停电炉失败：没有该电炉"
    if ovenid.currState == "pause":
        logger = logging.getLogger("django")
        logger.error("暂停电炉失败：该电炉已暂停")
        return "暂停电炉失败：该电炉已暂停"
    if ovenid.currState == "stop":
        logger = logging.getLogger("django")
        logger.error("暂停电炉失败：该电炉已停止")
        return "暂停电炉失败：该电炉已停止"
    if ovenid.nextState == "pause":
        logger = logging.getLogger("django")
        logger.error("暂停电炉失败：该电炉正在尝试暂停")
        return "正在尝试暂停......"
    ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="pause")
    logger = logging.getLogger("django")
    logger.info("暂停电炉：成功")
    return "暂停电炉成功！"


def resume_oven_interface(box_id, cha_id, oven_id, oven_scheme_id):
    try:
        ovenid = ovenDeviceTable.objects.get(ID=oven_id)
    except:
        logger = logging.getLogger("django")
        logger.error("继续电炉失败：没有该电炉")
        return "继续电炉失败：没有该电炉"
    if ovenid.currState == "start":
        logger = logging.getLogger("django")
        logger.error("继续电炉失败：该电炉已启动")
        return "继续电炉失败：该电炉已启动"
    if ovenid.currState == "stop":
        logger = logging.getLogger("django")
        logger.error("继续电炉失败：该电炉已停止")
        return "继续电炉失败：该电炉已停止"
    if ovenid.nextState == "start":
        logger = logging.getLogger("django")
        logger.error("继续电炉失败：该电炉正尝试启动")
        return "正在尝试启动......"
    ovenDeviceTable.objects.filter(ID=oven_id).update(nextState="start")
    logger = logging.getLogger("django")
    logger.info("继续电炉：成功")
    return "操作成功！"


def get_gas_info_interface(box_id, chn_id):
    testid = BigTestInfoTable.objects.filter(boxID=box_id, chnNum=chn_id, completeFlag=0)
    data = {'H2': -1, 'N2': -1, 'H2O': -1, 'Air': -1, 'CH4': -1, 'CO2': -1}
    if len(testid) == 0:
        logger = logging.getLogger("django")
        logger.error("getgasinfo:没有气体数据")
        return data
    elif len(testid) > 1:
        logger = logging.getLogger("django")
        logger.warning("getgasinfo:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        cellid = testid.cellID
    except:
        logger = logging.getLogger("django")
        logger.error("getgasinfo:没有找到该通道下的电池")
        return data
    data['H2'] = cellid.mH2ID.currState if cellid.mH2ID is not None else -1
    data['N2'] = cellid.mN2ID.currState if cellid.mN2ID is not None else -1
    data['H2O'] = cellid.mH2OID.currState if cellid.mH2OID is not None else -1
    data['CO2'] = cellid.mCO2ID.currState if cellid.mCO2ID is not None else -1
    data['CH4'] = cellid.mCH4ID.currState if cellid.mCH4ID is not None else -1
    data['Air'] = cellid.mAIRID.currState if cellid.mAIRID is not None else -1
    return data


def set_gas_interface(box_id, chn_id, data):
    testid = BigTestInfoTable.objects.filter(boxID=box_id, chnNum=chn_id, completeFlag=0)
    if len(testid) == 0:
        logger = logging.getLogger("django")
        logger.error("setgas:没有气体数据")
        return False
    elif len(testid) > 1:
        logger = logging.getLogger("django")
        logger.warning("setgas:当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        cellid = testid.cellID
    except:
        logger = logging.getLogger("django")
        logger.error("setgas:没有找到该通道下的电池")
        return False
    if data['H2'] is not None and cellid.mH2ID is not None:
        cellid.mH2ID.nextState = data['H2']
        cellid.mH2ID.save()
    if data['N2'] is not None and cellid.mN2ID is not None:
        cellid.mN2ID.nextState = data['N2']
        cellid.mN2ID.save()
    if data['CH4'] is not None and cellid.mCH4ID is not None:
        cellid.mCH4ID.nextState = data['CH4']
        cellid.mCH4ID.save()
    if data['Air'] is not None and cellid.mAIRID is not None:
        cellid.mAIRID.nextState = data['Air']
        cellid.mAIRID.save()
    if data['CO2'] is not None and cellid.mCO2ID is not None:
        cellid.mCO2ID.nextState = data['CO2']
        cellid.mCO2ID.save()
    if data['H2O'] is not None and cellid.mH2OID is not None:
        cellid.mH2OID.nextState = data['H2O']
        cellid.mH2OID.save()
    return True
