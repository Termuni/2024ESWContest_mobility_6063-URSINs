
import sys, os
import time

import UART_Communication as wcom


def Init_DMU():
    global CtD_Ser
    CtD_Ser = wcom.Init_UART(port="/dev/serial1") #CCU ~ DMU Serial
    
if __name__ == '__main__':
    Init_DMU()
    data_from_CCU = None
    data_to_CCU = "Hello CCU"
    try:
        while True:
            response_From_CCU = wcom.Slave_COM(CtD_Ser, data_from_CCU)
            response_To_CCU = wcom.Master_COM(CtD_Ser, data_to_CCU)

    except:
        wcom.Close_UART(CtD_Ser)
        print("END")