
import sys, os
import time

import UART_Communication as wcom


def Init_CCU():
    global CtT_Ser, DtC_Ser
    CtT_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    DtC_Ser = wcom.Init_UART(port="/dev/ttyAMA3") #CCU ~ DMU Serial
    
if __name__ == '__main__':
    Init_CCU()
    print(CtT_Ser)
    print(DtC_Ser)
    data_to_TCU = "Hello TCU\n"
    data_from_TCU = None
    data_from_DMU = None
    data_to_DMU = 'test\n'
    try:
        while True:
            data_from_TCU = wcom.Master_COM(CtT_Ser, data_to_TCU)
            data_from_DMU = wcom.Receive_Data_DMU(DtC_Ser) #Data from DMU (only Receive)
            print("Level_DMU :",data_from_DMU)
            print("Data_from_TCU :",data_from_TCU)
            time.sleep(0.01) 
    except:
        wcom.Close_UART(CtT_Ser)
        wcom.Close_UART(DtC_Ser)
        print("END")
