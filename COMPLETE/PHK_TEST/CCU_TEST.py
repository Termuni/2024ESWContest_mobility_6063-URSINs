
import sys, os
import time

import UART_Communication as wcom


def Init_CCU():
    global CtT_Ser, CtD_Ser
    CtT_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    CtD_Ser = wcom.Init_UART(port="/dev/serial1") #CCU ~ DMU Serial
    
if __name__ == '__main__':
    Init_CCU()
    data_to_TCU = "Hello TCU"
    data_to_DMU = "Hello DMU"
    data_from_TCU = None
    data_from_DMU = None
    try:
        while True:
            response_To_TCU = wcom.Master_COM(CtT_Ser, data_to_TCU)
            response_From_TCU = wcom.Slave_COM(CtT_Ser, data_from_TCU)
            response_To_DMU = wcom.Master_COM(CtD_Ser, data_to_DMU)
            response_From_DMU = wcom.Slave_COM(CtD_Ser, data_from_DMU)
    except:
        wcom.Close_UART(CtT_Ser)
        wcom.Close_UART(CtD_Ser)
        print("END")