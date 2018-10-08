from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, csv
import pymysql
import time

from .backend_db_interface import *

current_milli_time = lambda: int(round(time.time() * 1000))


# Create your views here.


def get_b_c_num(request):
    data = get_box_info_interface()
    return JsonResponse(data)


def monitor(request):
    return render(request, 'monitor.html')


def gas_control(request):
    return render(request, 'gas_control.html')


def oven_control(request):
    return render(request, 'oven_control.html')


# todo
def testline_status(request, box_num, channel_num):
    # run/pause/stop
    testid = testInfoTable.objects.filter(boxID=box_num, chnNum=channel_num)
    if len(testid) == 0:
        logging.error("testline-status找不到当前通道对应的测试信息")
        data = {"testline_status": "err"}
        return JsonResponse(data)
    elif len(testid) > 1:
        logging.error("testline-status当前通道有多条测试记录，选取最后一条")
    testid = testid.order_by("id").reverse()[0]
    try:
        crd = cellTestRealDataTable.objects.get(testID=testid)
        cs = crd.currState
    except:
        logging.error("testline-status当前通道无实时数据")
        cs = "stop"
    data = {"testline_status": cs}
    return JsonResponse(data)


def oven_status(request):
    data = get_oven_status_interface()
    return JsonResponse(data)


def cells_info(request):
    data = get_cells_info_interface()
    return JsonResponse(data)


def tests_info(request):
    data = get_tests_info_interface()
    return JsonResponse(data)


def get_testdata_from_start(request, box_num, channel_num):
    # 获取从测试开始的数据，返回一个具有多时间的数组
    # select scheme_num from scheme_table where box_num,channel_num
    # select data from history_data_table where box_num,channel_num,scheme_num
    # send data

    # data={"name": time.UTC(), "value":[UTC , value]}
    ##test
    data = get_history_test_data_interface(box_num, channel_num,
                                           test_id=get_latest_testid_interface(box_num, channel_num))
    ##test

    return JsonResponse(data)


def get_testdata_real_time(request, box_num, channel_num):
    # 获取实时数据，返回一条当前时间点的数据
    data = get_real_time_test_data_interface(box_num, channel_num)
    return JsonResponse(data)


def testline_info(request, box_num, channel_num):
    data = get_real_time_info_interface(box_num, channel_num)
    return JsonResponse(data)


def get_test_scheme(request, box_num, channel_num):
    # select * from schemeTable where box_num channel_num
    steps = []
    data = {
        "schemeID": 1,
        "steps": steps
    }
    data = get_current_scheme_interface(box_num, channel_num)
    return JsonResponse(data)


def control(request):
    return render(request, 'load_control.html')


def get_old_oven_scheme(request):
    ##test
    data = get_old_oven_test_scheme_interface()
    ##test
    return JsonResponse(data)


def get_old_scheme(request):
    ##test
    data = get_old_test_scheme_interface()
    ##test
    return JsonResponse(data)


def delete_old_scheme(request, num):
    return JsonResponse({"Message": "unknown"})


def delete_old_oven_scheme(request, num):
    return JsonResponse({"Message": "unknown"})


@csrf_exempt
def save_scheme(request):
    # print(request.body)
    # print(json.loads(request.body.decode()))
    scheme = json.loads(request.body.decode())
    if save_test_scheme_interface(scheme):
        logging.info("test-scheme保存成功")
        message = "保存成功"
    else:
        logging.error("test-scheme保存过程中出错")
        message = "保存过程中出错"
    return JsonResponse({"Message": message})


@csrf_exempt
def save_oven_scheme(request):
    # print(request.body)
    # print(json.loads(request.body.decode()))
    scheme = json.loads(request.body.decode())
    if save_oven_test_scheme_interface(scheme):
        logging.info("oven-scheme保存成功")
        message = "保存成功"
    else:
        logging.error("oven-scheme保存过程中出错")
        message = "保存过程中出错"
    return JsonResponse({"Message": message})


@csrf_exempt
def start_channel(request):
    datarecv = json.loads(request.body.decode())
    message = start_channel_interface(datarecv['box'], datarecv['channel'], datarecv['plan'])
    return JsonResponse({"Message": message})


@csrf_exempt
def start_oven(request):
    datarecv = json.loads(request.body.decode())
    message = start_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message": message})


@csrf_exempt
def stop_oven(request):
    datarecv = json.loads(request.body.decode())
    message = stop_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message": message})


@csrf_exempt
def pause_oven(request):
    datarecv = json.loads(request.body.decode())
    message = pause_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message": message})


@csrf_exempt
def resume_oven(request):
    datarecv = json.loads(request.body.decode())
    message = resume_oven_interface(datarecv['box'], datarecv['channel'], datarecv['oven'], datarecv['oplan'])
    return JsonResponse({"Message": message})


# @csrf_exempt
# def make_test(request):
#     datarecv = json.loads(request.body.decode())
#     print(datarecv)
#     make_test_interface(datarecv['box'], datarecv['channel'], datarecv['plan'], datarecv['oplan'])
#     return JsonResponse({})


@csrf_exempt
def pause_channel(request):
    datarecv = json.loads(request.body.decode())
    message = pause_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message": message})


@csrf_exempt
def stop_channel(request):
    datarecv = json.loads(request.body.decode())
    message = stop_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message": message})


@csrf_exempt
def continue_channel(request):
    datarecv = json.loads(request.body.decode())
    message = continue_channel_interface(datarecv['box'], datarecv['channel'])
    return JsonResponse({"Message": message})


def get_gas_info(request, box_id, chn_id):
    data = get_gas_info_interface(box_id, chn_id)
    return JsonResponse(data)


@csrf_exempt
def set_gas(request, box_id, chn_id):
    datarecv = json.loads(request.body.decode())
    if set_gas_interface(box_id, chn_id, datarecv):
        logging.info("气体设置成功")
        message = "气体设置成功"
    else:
        logging.info("气体设置失败！")
        message = "气体设置失败"
    return JsonResponse({"Message": message})


class IndexView(View):
    def get(self, request):
        customer = 'finacial'
        return render(request, "index.html", {
            "customer": customer,
        })


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@csrf_exempt
def data_export_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    if request.body.decode() == '':
        return render(request, 'data_export.html')
    if request.body.decode() == 'GetBigTestID':
        bts = BigTestInfoTable.objects.all()
        data = [bt.id for bt in bts]
        return JsonResponse({'BigTestID': data})
    a = request.body.decode()
    varlist = a.split('&')
    if "BigTestID=" not in varlist[0]:
        print('error')
        return render(request, 'data_export.html')
    btid = int(varlist[0].split('=')[1])
    print(btid)
    header = []
    for i in varlist[1:]:
        if "Variables=" not in i:
            print('error')
            return render(request, 'data_export.html')
        else:
            var = i.split('=')
            if len(var) == 2:
                if var[1] == 'u' or var[1] == 'i':
                    header = header + ["celldata_time", var[1]]
                elif var[1] in ["H2", "H2O", "CH4", "N2", "CO2", "AIR"]:
                    header = header + ["t" + var[1], "q" + var[1]]
                else:
                    header = header + ["t" + var[1], var[1]]
    historydata = cellTestHistoryDataTable.objects.filter(bigTestID_id=btid)
    rows = []
    rows.append(header)
    timeformat = lambda x: int(
        x.replace(tzinfo=timezone(timedelta(hours=TZ))).timestamp() * 1000) if x is not None else -1
    dataformat = lambda x: x if x is not None else -1
    for i in historydata:
        row = []
        for j in range(len(header)):
            if j % 2 == 0:
                row.append(timeformat(eval("i." + header[j])))
            else:
                row.append(dataformat(eval("i." + header[j])))
        rows.append(row)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="data_export.csv"'
    return response
