
import sys, os
import time

import UART_Communication as wcom


def Init_CCU():
    global cTt_Ser, dTc_Ser
    cTt_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    dTc_Ser = wcom.Init_UART(port="/dev/ttyAMA3") #CCU ~ DMU Serial
    
if __name__ == '__main__':
    Init_CCU()
    print(cTt_Ser)
    print(dTc_Ser)
    data_to_TCU = "Hello TCU\n"
    data_from_TCU = None
    data_from_DMU = None
    data_to_DMU = 'test\n'
    try:
        while True:
            data_from_TCU = wcom.Master_COM(cTt_Ser, data_to_TCU)
            data_from_DMU = wcom.Receive_Data_DMU(dTc_Ser) #Data from DMU (only Receive)
            print("Level_DMU :",data_from_DMU)
            print("Data_from_TCU :",data_from_TCU)
            time.sleep(0.01) 
    except:
        wcom.Close_UART(cTt_Ser)
        wcom.Close_UART(dTc_Ser)
        print("END")
