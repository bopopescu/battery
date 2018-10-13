from interfaces.HardwareProtocol import Oven_8,Oven_7
import signal
import socket
import time

for port in [20001,20002]:
    for addr in range(1,61):
        oven=Oven_8(addr)
        cmd=oven.buildcmdx(addr=0x00,mode="read")
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        ip = '192.168.0.4'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(0.5)
            s.connect((ip, port))
            try:
                s.send(cmd)
                try:
                    time.sleep(2)
                    data = s.recv(1000)
                    s.close()
                    if len(data) == 10:  # 帧长校验
                        PV = data[0] + (data[1] << 8)
                        SV = data[2] + (data[3] << 8)
                        MV = data[4] + (data[5] << 8)
                        value = data[6] + (data[7] << 8)
                        checksum = PV + SV + MV + value + oven.addr
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
                            data = {"PV": PV, "SV": SV, "MV": MV, "HIAL": HIAL, "LoAL": LoAL, "dHAL": dHAL, "dLAL": dLAL,
                                    "orAL": orAL,"AL1": AL1, "AL2": AL2, "VALUE": value}
                            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 成功！')
                            print(data)
                        else:
                            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据格式错误')
                    else:
                        print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据格式错误')
                except:  # 接收数据失败
                    print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据超时')
                    s.close()
            except:  # 读取数据失败
                print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 发送数据失败')
        except:  # 建立连接失败
            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 建立连接失败')