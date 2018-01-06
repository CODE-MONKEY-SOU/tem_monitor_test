from ctypes import *
from enum import *
import time

ECANdll = WinDLL("dll\\ECanVci64.dll")



class CanType(Enum):
    USB_CAN_I = 3
    USB_CAN_II = 4


class DevType(Enum):
    TEM_DEV = 1
    ELC_DEV = 2


class CanObj(Structure):
    _fields_ = [("ID", c_int),
                ("TimeStamp", c_int),
                ("TimeFlag", c_byte),
                ("SendType", c_byte),
                ("RemoteFlag", c_byte),
                ("ExternFlag", c_byte),
                ("DataLen", c_byte),
                ("Data", c_byte * 8),
                ("Reserved", c_byte * 3)]

    @classmethod
    def new_instance(cls, id, data, send_type=0, remote_flag=0, extern_flag=0, data_len=8):
        send_canobj = CanObj()
        send_canobj.ID = id
        send_canobj.SendType = send_type
        send_canobj.RemoteFlag = remote_flag
        send_canobj.ExternFlag = extern_flag
        send_canobj.DataLen = data_len
        send_canobj.Data = data
        return send_canobj


class CanStatus(Structure):
    _fields_ = [("ErrInterrupt", c_char),
                ("regMode", c_char),
                ("regStatus", c_char),
                ("regALCapture", c_char),
                ("regECCapture", c_char),
                ("regEWLimit", c_char),
                ("regRECounter", c_char),
                ("regTECounter", c_char),
                ("Reserved", c_long)]


class BoardInfo(Structure):
    _fields_ = [("hw_Version", c_short),
                ("fw_Version", c_short),
                ("dr_Version", c_short),
                ("in_Version", c_short),
                ("irp_Num", c_short),
                ("can_Num", c_byte),
                ("str_Serial_Num", c_char * 20),
                ("reserved", c_short * 4)]


class InitConfig(Structure):
    _fields_ = [("AccCode", c_int),
                ("AccMask", c_int),
                ("Reserved", c_int),
                ("Filter", c_char),
                ("Timing0", c_char),
                ("Timing1", c_char),
                ("Mode", c_char)]

    @classmethod
    def new_instance(cls, acc_code=0, acc_mask=int('0xFFFFFFFF', 16), filter=0, timing0=int('0x04', 16),
                    timing1=int('0x1C', 16), mode=0):
        initconfig = InitConfig()
        initconfig.AccCode = acc_code
        initconfig.AccMask = acc_mask
        initconfig.Filter = filter
        initconfig.Timing0 = timing0
        initconfig.Timing1 = timing1
        initconfig.Mode = mode
        return initconfig


def open_device(dev_index, dev_type=CanType.USB_CAN_II.value):
    odflag = ECANdll.OpenDevice(dev_type, dev_index, 0)
    time.sleep(0.01)
    return odflag == 1


def close_device(dev_index, dev_type=CanType.USB_CAN_II.value):
    cdflag = ECANdll.CloseDevice(dev_type, dev_index, 0)
    return cdflag == 1


def read_board_info(dev_index, p_info=BoardInfo(), dev_type=CanType.USB_CAN_II.value):
    ECANdll.ReadBoardInfo(dev_type, dev_index, byref(p_info))
    return p_info


def init_can(can_index, dev_index, init_config, dev_type=CanType.USB_CAN_II.value):
    icflag = ECANdll.InitCAN(dev_type, dev_index, can_index, byref(init_config))
    return icflag == 1


def read_can_status(can_index, dev_index, can_status=CanStatus(), dev_type=CanType.USB_CAN_II.value):
    ECANdll.ReadCANStatus(dev_type, dev_index, can_index, byref(can_status))
    return can_status


def start_can(dev_index, can_index, dev_type=CanType.USB_CAN_II.value):
    scflag = ECANdll.StartCAN(dev_type, dev_index, can_index)
    return scflag == 1


def transmit(dev_index, can_index, p_send, length, dev_type=CanType.USB_CAN_II.value):
    return ECANdll.Transmit(dev_type, dev_index, can_index, byref(p_send), length)


def receive(dev_index, can_index, p_receive, length, waittime, dev_type=CanType.USB_CAN_II.value):
    ECANdll.Receive(dev_type, dev_index, can_index, byref(p_receive), length, waittime)
    return p_receive


class Sensor:
    def __init__(self, can_index, dev_index, can_type):
        self.can_index = can_index
        self.dev_index = dev_index
        self.can_type = can_type

    def get_data(self):
        return 20
        # canobj = CAN_OBJ()
        # FuncReceive = ECANdll.Receive
        # nres = FuncReceive(self.can_type, self.dev_index, self.can_index, byref(canobj), 1, 1000)
        # return string_at(addressof(canobj.Data), sizeof(canobj.Data))


class TemperatureSensor(Sensor):
    def __init__(self, can_index, dev_index, can_type):
        Sensor.__init__(self, can_index, dev_index, can_type)
        self.dev_type = DevType.TEM_DEV.value

    def get_tem_data(self):
        self.get_data()


def main():
    open_device(0)

    a = read_board_info(0)
    print(a.str_Serial_Num)

    close_device(0)


if __name__ == '__main__':
    main()
