
import sys, os
import time

import UART_Communication as wcom


def Init_DMU():
    global CtD_Ser
    CtD_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ DMU Serial
    
if __name__ == '__main__':
    Init_DMU()
    data_from_CCU = None
    data_to_CCU = "25\n"
    try:
        while True:
            wcom.Send_Data(CtD_Ser, data_to_CCU)
            time.sleep(0.01)

    except:
        wcom.Close_UART(CtD_Ser)
        print("END")