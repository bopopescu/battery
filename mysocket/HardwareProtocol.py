import datetime
import logging


class Oven_7(object):
    addr = 0x01
    valDict = {"SV/SteP": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "dF": 0x05, "CtrL": 0x06,
               "M5": 0x07, "P": 0x08, "t": 0x09, "CtI": 0x0A, "Sn": 0x0B, "dIP": 0x0C, "dIL": 0x0D, "dIH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oPt": 0x11, "oPL": 0x12, "oPH": 0x13, "CF": 0x14, "r/h/s": 0x15, "Addr": 0x16,
               "dL": 0x17, "run": 0x18, "Loc": 0x19, "runtime": 0x56}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(0, 30):
            self.valDict["C" + str(i + 1)] = 0x1A + 0x02 * i
            self.valDict["t" + str(i + 1)] = 0x1B + 0x02 * i

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven7-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None


class Oven_8(object):
    addr = 0x01
    valDict = {"SV": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "AHYS": 0x05, "CtrL": 0x06,
               "P": 0x07, "I": 0x08, "d": 0x09, "Ctl": 0x0A, "InP": 0x0B, "dPt": 0x0C, "ScL": 0x0D, "ScH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oP1": 0x11, "OPL": 0x12, "OPH": 0x13, "CF": 0x14, "type": 0x15, "Addr": 0x16,
               "FILt": 0x17, "AMAn": 0x18, "Loc": 0x19, "MV": 0x1A, "Srun": 0x1B, "CHYS": 0x1C, "At": 0x1D,
               "SPL": 0x1E, "SPH": 0x1F, "Fru": 0x20, "OHFE OPH": 0x21, "Act": 0x22, "AdIS": 0x23, "Aut": 0x24,
               "P2": 0x25, "I2": 0x26, "d2": 0x27, "Ctl2": 0x28, "Et": 0x29, "SPr": 0x2A, "Pno": 0x2B, "PonP": 0x2C,
               "PAF": 0x2D, "STEP": 0x2E, "runtime": 0x2F, "eventoutput": 0x30, "OPrt": 0x31, "Strt": 0x32,
               "SPSL": 0x33, "SPSH": 0x34, "Ero": 0x35, "AF2": 0x36, "EP1": 0x40, "EP2": 0x41, "EP3": 0x42,
               "EP4": 0x43, "EP5": 0x44, "EP6": 0x45, "EP7": 0x46, "EP8": 0x47, "C1": 0x50, "t1": 0x51}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(2, 31):
            self.valDict["C" + str(i)] = 0x50 + 0x02 * (i - 1)
            self.valDict["t" + str(i)] = 0x51 + 0x02 * (i - 1)

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven8-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None


class Wdj_7(object):
    addr = 0x01
    valDict = {"SV/SteP": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "dF": 0x05, "CtrL": 0x06,
               "M5": 0x07, "P": 0x08, "t": 0x09, "CtI": 0x0A, "Sn": 0x0B, "dIP": 0x0C, "dIL": 0x0D, "dIH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oPt": 0x11, "oPL": 0x12, "oPH": 0x13, "CF": 0x14, "r/h/s": 0x15, "Addr": 0x16,
               "dL": 0x17, "run": 0x18, "Loc": 0x19, "runtime": 0x56}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(0, 30):
            self.valDict["C" + str(i + 1)] = 0x1A + 0x02 * i
            self.valDict["t" + str(i + 1)] = 0x1B + 0x02 * i

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven7-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None


class Wdj_8(object):
    addr = 0x01
    valDict = {"SV": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "AHYS": 0x05, "CtrL": 0x06,
               "P": 0x07, "I": 0x08, "d": 0x09, "Ctl": 0x0A, "InP": 0x0B, "dPt": 0x0C, "ScL": 0x0D, "ScH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oP1": 0x11, "OPL": 0x12, "OPH": 0x13, "CF": 0x14, "type": 0x15, "Addr": 0x16,
               "FILt": 0x17, "AMAn": 0x18, "Loc": 0x19, "MV": 0x1A, "Srun": 0x1B, "CHYS": 0x1C, "At": 0x1D,
               "SPL": 0x1E, "SPH": 0x1F, "Fru": 0x20, "OHFE OPH": 0x21, "Act": 0x22, "AdIS": 0x23, "Aut": 0x24,
               "P2": 0x25, "I2": 0x26, "d2": 0x27, "Ctl2": 0x28, "Et": 0x29, "SPr": 0x2A, "Pno": 0x2B, "PonP": 0x2C,
               "PAF": 0x2D, "STEP": 0x2E, "runtime": 0x2F, "eventoutput": 0x30, "OPrt": 0x31, "Strt": 0x32,
               "SPSL": 0x33, "SPSH": 0x34, "Ero": 0x35, "AF2": 0x36, "EP1": 0x40, "EP2": 0x41, "EP3": 0x42,
               "EP4": 0x43, "EP5": 0x44, "EP6": 0x45, "EP7": 0x46, "EP8": 0x47, "SP1": 0x50, "t1": 0x51}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(2, 31):
            self.valDict["SP" + str(i)] = 0x50 + 0x02 * (i - 1)
            self.valDict["t" + str(i)] = 0x51 + 0x02 * (i - 1)

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven8-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None


class Volt_7(object):
    addr = 0x01
    valDict = {"SV/SteP": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "dF": 0x05, "CtrL": 0x06,
               "M5": 0x07, "P": 0x08, "t": 0x09, "CtI": 0x0A, "Sn": 0x0B, "dIP": 0x0C, "dIL": 0x0D, "dIH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oPt": 0x11, "oPL": 0x12, "oPH": 0x13, "CF": 0x14, "r/h/s": 0x15, "Addr": 0x16,
               "dL": 0x17, "run": 0x18, "Loc": 0x19, "runtime": 0x56}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(0, 30):
            self.valDict["C" + str(i + 1)] = 0x1A + 0x02 * i
            self.valDict["t" + str(i + 1)] = 0x1B + 0x02 * i

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven7-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven7-mode错误 只能为read/set")
            return None


class Volt_8(object):
    addr = 0x01
    valDict = {"SV": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "AHYS": 0x05, "CtrL": 0x06,
               "P": 0x07, "I": 0x08, "d": 0x09, "Ctl": 0x0A, "InP": 0x0B, "dPt": 0x0C, "ScL": 0x0D, "ScH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oP1": 0x11, "OPL": 0x12, "OPH": 0x13, "CF": 0x14, "type": 0x15, "Addr": 0x16,
               "FILt": 0x17, "AMAn": 0x18, "Loc": 0x19, "MV": 0x1A, "Srun": 0x1B, "CHYS": 0x1C, "At": 0x1D,
               "SPL": 0x1E, "SPH": 0x1F, "Fru": 0x20, "OHFE OPH": 0x21, "Act": 0x22, "AdIS": 0x23, "Aut": 0x24,
               "P2": 0x25, "I2": 0x26, "d2": 0x27, "Ctl2": 0x28, "Et": 0x29, "SPr": 0x2A, "Pno": 0x2B, "PonP": 0x2C,
               "PAF": 0x2D, "STEP": 0x2E, "runtime": 0x2F, "eventoutput": 0x30, "OPrt": 0x31, "Strt": 0x32,
               "SPSL": 0x33, "SPSH": 0x34, "Ero": 0x35, "AF2": 0x36, "EP1": 0x40, "EP2": 0x41, "EP3": 0x42,
               "EP4": 0x43, "EP5": 0x44, "EP6": 0x45, "EP7": 0x46, "EP8": 0x47, "SP1": 0x50, "t1": 0x51}

    def __init__(self, addr=0x01):
        self.addr = addr
        for i in range(2, 31):
            self.valDict["SP" + str(i)] = 0x50 + 0x02 * (i - 1)
            self.valDict["t" + str(i)] = 0x51 + 0x02 * (i - 1)

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            logging.error("protocol-oven8-没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            logging.error("protocol-oven8-mode错误 只能为read/set")
            return None


class MFC(object):
    addr = 0x20  # 0x20~0x5F 0xFF为广播地址，所有设备都产生响应

    def __init__(self, addr=0x20):
        self.addr = addr

    def buildcmd(self, type, value=0x00):
        if type == 'SetCM':
            # 1代表由485控制，2、3代表由模拟量控制
            stype = 0x81
            length=0x04
            dataclass=0x69
            datainstance=0x01
            dataattribute=0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum=checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetDefaultCM':
            # 1代表由485控制，2、3代表由模拟量控制
            stype = 0x81
            length = 0x04
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x04
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetEEPROMProgram':
            stype = 0x81
            length = 0x04
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x06
            value = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadCM':
            # 1代表由485控制，2、3代表由模拟量控制
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadDefaultCM':
            # 1代表由485控制，2、3代表由模拟量控制
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x04
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetHoldFollow':
            stype = 0x81
            length = 0x04
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x05
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetDelay':
            stype = 0x81
            length = 0x05
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0xA6
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetDigitalSetpoint':
            stype = 0x81
            length = 0x05
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0xA4
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetSoftstartRate':
            stype = 0x81
            length = 0x05
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA4
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetShutoffLevel':
            stype = 0x81
            length = 0x05
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA2
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadHoldFollow':
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0x05
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadDelay':
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0xA6
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadDigitalSetpoint':
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0xA4
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadActiveSetpoint':
            stype = 0x80
            length = 0x03
            dataclass = 0x69
            datainstance = 0x01
            dataattribute = 0xA5
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadSoftstartRate':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA4
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadShutoffLevel':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA2
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetZeroStatus':
            stype = 0x81
            length = 0x04
            dataclass = 0x68
            datainstance = 0x01
            dataattribute = 0xBA
            value = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadFlow':
            stype = 0x80
            length = 0x03
            dataclass = 0x68
            datainstance = 0x01
            dataattribute = 0xB9
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetValveCommandMode':
            stype = 0x81
            length = 0x04
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA1
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetValveCommand':
            stype = 0x81
            length = 0x04
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadValveCommandMode':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0xA1
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadValveCommand':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadValveVoltage':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0x91
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadValveType':
            stype = 0x80
            length = 0x03
            dataclass = 0x6A
            datainstance = 0x01
            dataattribute = 0x9C
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetControlledFlowAccumulatorMode':
            stype = 0x81
            length = 0x04
            dataclass = 0xA4
            datainstance = 0x01
            dataattribute = 0x05
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadControlledFlowAccumulatorMode':
            stype = 0x80
            length = 0x03
            dataclass = 0xA4
            datainstance = 0x01
            dataattribute = 0x05
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadControlledFlowAccumulator':
            stype = 0x80
            length = 0x03
            dataclass = 0xA4
            datainstance = 0x01
            dataattribute = 0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetEnable/DisableWarningAndAlarm':
            stype = 0x81
            length = 0x05
            dataclass = 0x65
            datainstance = 0x01
            dataattribute = 0xA2
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetClearWarningAndAlarm':
            stype = 0x81
            length = 0x04
            dataclass = 0x65
            datainstance = 0x01
            dataattribute = 0xA1
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadWarningAndAlarm':
            stype = 0x80
            length = 0x03
            dataclass = 0x65
            datainstance = 0x01
            dataattribute = 0xA0
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadEnable/DisableWarningAndAlarm':
            stype = 0x80
            length = 0x03
            dataclass = 0x65
            datainstance = 0x01
            dataattribute = 0xA2
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'ReadProductName':
            stype = 0x80
            length = 0x03
            dataclass = 0x01
            datainstance = 0x01
            dataattribute = 0x07
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadRevisionCode':
            stype = 0x80
            length = 0x03
            dataclass = 0x01
            datainstance = 0x01
            dataattribute = 0x04
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadManufacturer':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadModelIdentifier':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x04
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadFirmwareRevision':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x05
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadPCBRevision':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x06
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadMFCSerialNumber':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x07
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadManufacturingDate':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x0A
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadCalibrationDate':
            stype = 0x80
            length = 0x03
            dataclass = 0x64
            datainstance = 0x01
            dataattribute = 0x0C
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                    0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetTargetGasCode':
            stype = 0x81
            length = 0x05
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x02
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetTargetGasFullScaleRange':
            stype = 0x81
            length = 0x05
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x03
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadTargetGasCode':
            stype = 0x80
            length = 0x03
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x02
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadTargetGasFullScaleRange':
            stype = 0x80
            length = 0x03
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadCalibrationGasCode':
            stype = 0x80
            length = 0x03
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x07
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadCalibrationGasFullScaleRange':
            stype = 0x80
            length = 0x03
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x08
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadCalibrationTemperature':
            stype = 0x80
            length = 0x03
            dataclass = 0x66
            datainstance = 0x01
            dataattribute = 0x0A
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'SetTargetNullValue':
            stype = 0x81
            length = 0x07
            dataclass = 0xA1
            datainstance = 0x01
            dataattribute = 0x07
            value1 = value & 0x000000ff
            value2 = (value & 0x0000ff00) >> 8
            value3 = (value & 0x00ff0000) >> 16
            value4 = (value & 0xff000000) >> 32
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value1 + value2 + value3 + value4 + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value1, value2, value3, value4, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'ReadTargetNullValue':
            stype = 0x80
            length = 0x03
            dataclass = 0xA1
            datainstance = 0x01
            dataattribute = 0x07
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'ReadTemperature':
            stype = 0x80
            length = 0x03
            dataclass = 0xA3
            datainstance = 0x01
            dataattribute = 0x07
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        elif type == 'Set485Addr':
            stype = 0x81
            length = 0x04
            dataclass = 0x03
            datainstance = 0x01
            dataattribute = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'Set485BaudRate':
            stype = 0x81
            length = 0x05
            dataclass = 0x03
            datainstance = 0x01
            dataattribute = 0x02
            valuelo = value & 0x00ff
            valuehi = (value & 0xff00) >> 8
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + valuelo + valuehi + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   valuelo, valuehi, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'SetReset':
            stype = 0x81
            length = 0x04
            dataclass = 0x03
            datainstance = 0x01
            dataattribute = 0x03
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + value + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   value, 0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'Read485Addr':
            stype = 0x80
            length = 0x03
            dataclass = 0x03
            datainstance = 0x01
            dataattribute = 0x01
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd
        elif type == 'Read485BaudRate':
            stype = 0x80
            length = 0x03
            dataclass = 0x03
            datainstance = 0x01
            dataattribute = 0x02
            checksum = self.addr + 0x02 + stype + length + dataclass + datainstance + dataattribute + 0x00
            checksum = checksum & 0x000000ff
            cmd = [self.addr, 0x02, stype,
                   length, dataclass, datainstance, dataattribute,
                   0x00, checksum]
            cmd = bytearray(cmd)
            return cmd

        else:
            logging.error("protocol-MFC-type错误")
            return None


class eLoad(object):
    plan = None
    boxid = None
    chnnum = None

    def __init__(self, boxid, chnnum, plan):
        self.plan = plan
        self.boxid = boxid
        self.chnnum = chnnum

    def checksum(self, data):
        sum = 0
        length = data[2] + (data[3] << 8)
        for i in range(length - 2):
            sum = sum + data[4 + i]
        return sum

    def buildcmd(self, cmdtype):
        if (cmdtype == 'start'):
            # 构造命令
            totalStep = len(self.plan)
            length = totalStep * 40 + 309 + 98
            CMD = bytearray()
            for i in range(length):
                CMD.append(0x0)

            # 构造报文头
            CMD[0] = 0xAA
            CMD[1] = 0x55
            CMD[2] = (length - 6) & 0xFF
            CMD[3] = ((length - 6) & 0xFF00) >> 8
            CMD[4] = 0x92
            CMD[5] = 0

            # 更新箱号
            CMD[6] = self.boxid
            # 命令号
            CMD[7] = 0x06

            # 更新通道号
            chnInt = self.chnnum // 8
            chnRes = self.chnnum % 8
            CMD[8 + chnInt] = 0x01 << chnRes  # Q1

            # 测试方案ID号
            nowTime = datetime.now()
            CMD[40] = nowTime.year - 2000  # year
            CMD[41] = nowTime.month  # month
            CMD[42] = nowTime.day  # day
            CMD[43] = 0  # boxid
            CMD[44] = 0  # chnnum
            CMD[45] = 0x0F  # seq

            # 启动时间
            CMD[46] = nowTime.year - 2000  # year
            CMD[47] = nowTime.month  # month
            CMD[48] = nowTime.day  # day
            CMD[49] = nowTime.hour  # hour
            CMD[50] = nowTime.minute  # min
            CMD[51] = nowTime.second  # sec

            # 测试过程编程
            CMD[304] = totalStep

            for j in range(totalStep):
                CMD[305 + 40 * j] = j + 1  # 当前工步号从1开始
                # 计算限制条件数
                n_limit = {}
                if self.plan[j]['tTH'] is not None and self.plan[j]['tTH'] != 0:
                    n_limit.update({"tTH": self.plan[j]['tTH']})
                if self.plan[j]['uTH'] is not None and self.plan[j]['uTH'] != 0:
                    n_limit.update({"uTH": self.plan[j]['uTH']})
                if self.plan[j]['iTH'] is not None and self.plan[j]['iTH'] != 0:
                    n_limit.update({"iTH": self.plan[j]['iTH']})
                if self.plan[j]['qTH'] is not None and self.plan[j]['qTH'] != 0:
                    n_limit.update({"qTH": self.plan[j]['qTH']})
                limit_code = {"tTH": 0x11, "uTH": 0x22, "iTH": 0x33, "qTH": 0x44, "qATH": 0x55, "None": 0xF1}
                for i in range(5):  # 首先置空所有的限制条件
                    CMD[305 + 40 * j + 10 + 5 * i] = 0xF1  # 无限制条件
                    CMD[305 + 40 * j + 11 + 5 * i] = 0  # 限制条件 4个字节
                    CMD[305 + 40 * j + 12 + 5 * i] = 0  # 限制条件 4个字节
                    CMD[305 + 40 * j + 13 + 5 * i] = 0  # 限制条件 4个字节
                    CMD[305 + 40 * j + 14 + 5 * i] = 0  # 限制条件 4个字节
                n = 0
                for i in n_limit.keys():
                    CMD[305 + 40 * j + 10 + 5 * n] = limit_code[i]  # 限制条件n
                    CMD[305 + 40 * j + 11 + 5 * n] = (n_limit[i] & 0xFF000000) >> 24  # 限制条件 4个字节
                    CMD[305 + 40 * j + 12 + 5 * n] = (n_limit[i] & 0xFF0000) >> 16  # 限制条件 4个字节
                    CMD[305 + 40 * j + 13 + 5 * n] = (n_limit[i] & 0xFF00) >> 8  # 限制条件 4个字节
                    CMD[305 + 40 * j + 14 + 5 * n] = (n_limit[i] & 0xFF)  # 限制条件 4个字节
                    n = n + 1

                if self.plan[j]['mode'] == '静置':  # 00 71 B1 18
                    CMD[305 + 40 * j + 1] = 0x01  # 工作模式
                    CMD[305 + 40 * j + 2] = 0  # (config.plan[j]['tTH']&0xFF000000)>>24	#主参数 4个字节
                    CMD[305 + 40 * j + 3] = 0x71  # (config.plan[j]['tTH']&0xFF0000)>>16	#主参数 4个字节
                    CMD[305 + 40 * j + 4] = 0xB1  # (config.plan[j]['tTH']&0xFF00)>>8		#主参数 4个字节
                    CMD[305 + 40 * j + 5] = 0x18  # (config.plan[j]['tTH']&0xFF)			#主参数 4个字节

                    CMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                    CMD[305 + 40 * j + 35] = 0x11  # 记录条件
                    CMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                    CMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                elif self.plan[j]['mode'] == '恒流充电':
                    CMD[305 + 40 * j + 1] = 0x02  # 工作模式
                    CMD[305 + 40 * j + 2] = (self.plan[j]['i'] & 0xFF000000) >> 24  # 主参数 4个字节
                    CMD[305 + 40 * j + 3] = (self.plan[j]['i'] & 0xFF0000) >> 16  # 主参数 4个字节
                    CMD[305 + 40 * j + 4] = (self.plan[j]['i'] & 0xFF00) >> 8  # 主参数 4个字节
                    CMD[305 + 40 * j + 5] = (self.plan[j]['i'] & 0xFF)  # 主参数 4个字节

                    CMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                    CMD[305 + 40 * j + 35] = 0x11  # 记录条件
                    CMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                    CMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                elif self.plan[j]['mode'] == '恒流放电':
                    CMD[305 + 40 * j + 1] = 0x03  # 工作模式
                    CMD[305 + 40 * j + 2] = (self.plan[j]['i'] & 0xFF000000) >> 24  # 主参数 4个字节
                    CMD[305 + 40 * j + 3] = (self.plan[j]['i'] & 0xFF0000) >> 16  # 主参数 4个字节
                    CMD[305 + 40 * j + 4] = (self.plan[j]['i'] & 0xFF00) >> 8  # 主参数 4个字节
                    CMD[305 + 40 * j + 5] = (self.plan[j]['i'] & 0xFF)  # 主参数 4个字节

                    CMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                    CMD[305 + 40 * j + 35] = 0x11  # 记录条件
                    CMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                    CMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                elif self.plan[j]['mode'] == '恒压充电':
                    CMD[305 + 40 * j + 1] = 0x04  # 工作模式
                    CMD[305 + 40 * j + 2] = (self.plan[j]['u'] & 0xFF000000) >> 24  # 主参数 4个字节
                    CMD[305 + 40 * j + 3] = (self.plan[j]['u'] & 0xFF0000) >> 16  # 主参数 4个字节
                    CMD[305 + 40 * j + 4] = (self.plan[j]['u'] & 0xFF00) >> 8  # 主参数 4个字节
                    CMD[305 + 40 * j + 5] = (self.plan[j]['u'] & 0xFF)  # 主参数 4个字节

                    CMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                    CMD[305 + 40 * j + 35] = 0x11  # 记录条件
                    CMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                    CMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                elif self.plan[j]['mode'] == '恒压放电':
                    CMD[305 + 40 * j + 1] = 0x05  # 工作模式
                    CMD[305 + 40 * j + 2] = (self.plan[j]['u'] & 0xFF000000) >> 24  # 主参数 4个字节
                    CMD[305 + 40 * j + 3] = (self.plan[j]['u'] & 0xFF0000) >> 16  # 主参数 4个字节
                    CMD[305 + 40 * j + 4] = (self.plan[j]['u'] & 0xFF00) >> 8  # 主参数 4个字节
                    CMD[305 + 40 * j + 5] = (self.plan[j]['u'] & 0xFF)  # 主参数 4个字节

                    CMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                    CMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                    CMD[305 + 40 * j + 35] = 0x11  # 记录条件
                    CMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                    CMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                    CMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                else:
                    print("buildCMD_box_start: unknown plan[mode] return None")
                    return None
                # elif self.plan[j]['mode'] == '恒压限流充电':
                #     pass
                # elif self.plan[j]['mode'] == '恒压限流放电':
                #     pass
                # elif self.plan[j]['mode'] == '恒阻放电':
                #     pass
                # elif self.plan[j]['mode'] == '恒功率放电':
                #     pass
                # elif self.plan[j]['mode'] == '恒功率充电':
                #     pass
                # elif self.plan[j]['mode'] == '循环':
                #     pass
                # elif self.plan[j]['mode'] == '跳转':
                #     pass
                # elif self.plan[j]['mode'] == '电压采样':
                #     pass

            # 总的记录条件
            CMD[305 + 40 * totalStep] = 0  # 记录条件
            CMD[305 + 40 * totalStep + 1] = 0  # 记录条件 4个字节
            CMD[305 + 40 * totalStep + 2] = 0  # 记录条件 4个字节
            CMD[305 + 40 * totalStep + 3] = 0  # 记录条件 4个字节
            # 更新校验和
            sum = self.checksum(CMD)
            CMD[-4] = sum & 0xFF
            CMD[-3] = (sum & 0xFF00) >> 8
            # 构造报文尾
            CMD[-1] = 0xAA
            CMD[-2] = 0x55
            return CMD

        elif (cmdtype == 'stop'):
            # 构造命令
            CMD = bytearray(
                [0xAA, 0x55, 0x26, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x55, 0xAA])

            # 更新箱号
            CMD[6] = self.boxid
            # CMD[6] = 0
            # 更新通道号
            chnInt = self.chnnum // 8
            chnRes = self.chnnum % 8
            CMD[8 + chnInt] = 0x01 << chnRes

            # 更新校验和
            sum = self.checksum(CMD)
            CMD[-4] = sum & 0xFF
            CMD[-3] = (sum & 0xFF00) >> 8

            return CMD

        elif (cmdtype == 'resume'):
            # 构造命令
            CMD = bytearray(
                [0xAA, 0x55, 0x27, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x55, 0xAA])
            # 更新箱号
            CMD[6] = self.boxid
            # CMD[6] = 0
            # 更新暂停命令
            CMD[8] = 0xFF  # 0x0暂停 0xff继续

            # 更新通道号
            chnInt = self.chnnum // 8
            chnRes = self.chnnum % 8
            CMD[9 + chnInt] = 0x1 << chnRes

            # 更新校验和
            sum = self.checksum(CMD)
            CMD[-4] = sum & 0xFF
            CMD[-3] = (sum & 0xFF00) >> 8

            return CMD

        elif (cmdtype == 'pause'):
            # 构造命令
            CMD = bytearray(
                [0xAA, 0x55, 0x27, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x55, 0xAA])

            # 更新箱号
            CMD[6] = self.boxid
            # CMD[6] = 0
            # 更新暂停命令
            CMD[8] = 0  # 暂停

            # 更新通道号
            chnInt = self.chnnum // 8
            chnRes = self.chnnum % 8
            CMD[9 + chnInt] = 0x1 << chnRes

            # 更新校验和
            sum = self.checksum(CMD)
            CMD[-4] = sum & 0xFF
            CMD[-3] = (sum & 0xFF00) >> 8

            return CMD

        elif (cmdtype == 'read'):
            # 构造命令
            CMD = bytearray(
                [0xAA, 0x55, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00,
                 0x55, 0xAA])
            # 更新箱号
            CMD[6] = self.boxid
            # readBoxRealDataCMD[6] = 0
            # 更新校验和
            sum = self.checksum(CMD)
            CMD[-4] = sum & 0xFF
            CMD[-3] = (sum & 0xFF00) >> 8

            return CMD

        else:
            print("BulidCMD_BOX: unknown config.cmd")
            return None


class MFC_alicat(object):
    addr = None

    def __init__(self, addr):
        self.addr = addr

    def buildcmd(self, type, value=0):
        if type == 'set':  # 'addr'+'S'+'value'+'\r'
            cmd = bytearray([ord(self.addr), 0x53])
            nextState = str(value).encode(encoding='ascii')
            for i in nextState:
                cmd.append(i)
            cmd.append(0x0D)
            return cmd
        elif type == 'read':
            cmd = bytearray([ord(self.addr), 0x0D])  # A\r
            return cmd
        else:
            print("BulidCMD_GAS: unknown type")
            return None



if __name__=='__main__':
    m=MFC(0x22)
    print(m.buildcmd(type='ReadFlow'))