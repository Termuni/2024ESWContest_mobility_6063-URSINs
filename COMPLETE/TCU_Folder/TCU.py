#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import numpy as np
import sys
sys.path.append(os.path.dirname(os.path.dirname(__path__)))

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import UART_Communication as wcom
#==================CUSTOM IMPORT==================

#Init
def Init_TCU():
    global GPIO
    global cTt_Ser, data_to_CCU, data_from_CCU
    global debug_mode, mode_change_input, wheel_value, warning_LV
    # 1. SET GPIO
    GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
       
    # 2. Init Communication
    cTt_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    data_to_CCU = "0,0"
    data_from_CCU = None
    
    # 3. SET extra Datas
    debug_mode = False
    mode_change_input = False
    warning_LV = 0
    wheel_value = [0, 0]


#====================Main==================

try:
    #INIT VALUES
    Init_TCU()

    print("ACTIVE PROCESSING")
    while True:
        
        data_from_CCU = wcom.Receive_Data(cTt_Ser)
        warning_LV = int(data_from_CCU)
        
        #If Debug Mode
        if mode_change_input:
            mode_change_input = not mode_change_input
            
            if debug_mode:
                print("DEBUG MODE ACTIVATE")
            
            else:
                #Else Getting Sensor Value
                print("DEBUG MODE DEACTIVATE")
                
        
        #If Warning Lv 2
        if warning_LV == 2:
            #Streaming Inside CAM
            print("Streaming Inside CAM")
        
        
        
        #If Warning Lv 3
        if warning_LV == 3:
            #Get Data From Center
            #Streaming Outside CAM
            print("Streaming Outside CAM")
            #Sending Handling Data to CCU
            data_to_CCU = f'{wheel_value[0]},{wheel_value[1]}'
            wcom.Send_Data(cTt_Ser, data_to_CCU)
        
        
        print("")
        
except:
    print("END")
    
finally:
    print("CLEAN")