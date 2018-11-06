from interfaces.HardwareProtocol import eLoad
import signal
import socket
import time

for port in [20004, ]:
    for addr in range(0,1):
        cellplan=[{"id":1, "planID_id":1, "step":1, "mode":"静置", "i":0, "u":0, "r":0, "p":0, "n":0, "nStart":0, "nStop":0, "nTarget":0, "tTH":0, "iTH":0,
                "uTH":0, "qTH":0},]
        load = eLoad(boxid=0, chnnum=0,plan=cellplan)
        cmd = load.buildcmd("read")
        print(list(cmd))
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        ip = '192.168.0.4'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)
            s.connect((ip, port))
            try:
                s.send(cmd)
                try:
                    time.sleep(2)
                    data = s.recv(4000)
                    print(len(data))
                    s.close()
                    if True:
                        if len(data) == 3471:  # 数据长度校验
                            DataDict = {}
                            i = load.chnnum
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
                            print(DataDict)
                        else:
                            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据长度错误')
                        print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 成功！')
                    else:
                        print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据格式错误')
                except:  # 接收数据失败
                    print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据超时')
                    s.close()
            except:  # 读取数据失败
                print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 发送数据失败')
        except:  # 建立连接失败
            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 建立连接失败')
