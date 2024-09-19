
import sys, os
import time

import UART_Communication as wcom


def Init_TCU():
    global CtT_Ser
    CtT_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    
if __name__ == '__main__':
    Init_TCU()
    data_from_CCU = None
    data_to_CCU = "Hello CCUsadds\n"
    try:
        while True:
            data_from_CCU = wcom.Slave_COM(CtT_Ser, data_to_CCU)
            print("Data from CCU :",data_from_CCU)
            time.sleep(0.01)

    except:
        wcom.Close_UART(CtT_Ser)
        print("END")