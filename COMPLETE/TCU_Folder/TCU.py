#import
import sys, os
#import RPi.GPIO as GPIO 
import serial
import time
import numpy as np
import sys
#sys.path.append(os.path.dirname(os.path.dirname(__path__)))

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import UART_Communication as wcom
#import Streaming as strm
#==================CUSTOM IMPORT==================

#Init
def Init_TCU():
    #global GPIO
    global client_Socket, cTt_Ser, data_to_CCU, data_from_CCU, HOST, PORT
    global remote_Active, debug_mode, mode_change_input, wheel_value, warning_LV
    # 1. SET GPIO
    #GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
       
    # 2. Init Communication
    HOST = '10.211.173.2'  # server VPN IP
    PORT = 9091  #
    client_Socket = wlcom.Init_Client_Socket(HOST, PORT)
    cTt_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    data_to_CCU = "0,0"
    data_from_CCU = '0'
    print("COMPLETE COM")
    
    # . Init Streaming
    #strm.Setup_Camera()
    
    # 3. SET extra Datas
    remote_Active = False
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
        cTt_Ser.reset_input_buffer()
        time.sleep(0.01)
        
        
        data_to_Center = data_from_CCU
        wlcom.Send_Socket(client_Socket, data_to_Center)
        
        data_from_Center = wlcom.Receive_Socket(client_Socket).decode()
        center_data = data_from_Center.split(',')
        
        if (data_from_CCU != '') and (data_from_CCU.isdecimal()):
            warning_LV = int(data_from_CCU)
        
        
        if (data_from_Center != '') and (len(center_data) == 3) :
            if ((center_data[0].isdecimal) and (center_data[1].isdecimal())) and (center_data[2].isdecimal()):
                if int(center_data[0]) == 4:
                    remote_Active = True
                wheel_value[0] = center_data[1]
                wheel_value[1] = center_data[2]
            
        
        
        print(warning_LV, wheel_value)
        
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
            #strm.Start_UV4L_Service()
        
        #If Warning Lv 3
        elif warning_LV == 3:
            #Get Data From Center
            #Streaming Outside CAM
            print("Streaming Outside CAM")
            
        if remote_Active:
            data_to_CCU = f'{4},{wheel_value[0]},{wheel_value[1]}'
            wcom.Send_Data(cTt_Ser, data_to_CCU)
            
        time.sleep(0.05)
        
except Exception as e:
    print("Error! :",e)
    wlcom.Close_Socket(client_Socket)
    #strm.Stop_UV4L_Service()
    print("END")
    
finally:
    
    print("CLEAN")
