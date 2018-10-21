from interfaces.HardwareProtocol import MFC
import signal
import socket
import time

for port in [20003,]:
    for addr in range(0x20,0x24):
        mfc=MFC(addr)
        cmd=mfc.buildcmd(type='ReadFlow')
        #cmd=mfc.buildcmd(type="SetDigitalSetpoint", value=0x4000)
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
                    print(data)
                    s.close()
                    if len(data) == 12 and data[0] == 0x06:  # 帧长校验
                        result = (data[8] + (data[9] << 8) - 0x4000) / (0xc000 - 0x4000)
                        print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 成功！')
                        print(result)
                    else:
                        print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据格式错误')
                except Exception as e:  # 接收数据失败
                    print(e)
                    print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 接收数据超时')
                    s.close()
            except:  # 读取数据失败
                print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 发送数据失败')
        except:  # 建立连接失败
            print('485地址:' + str(addr) + '   IP:' + ip + '   Port:' + str(port) + ' 建立连接失败')