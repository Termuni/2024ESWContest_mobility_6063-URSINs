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
import GPS_TCU as gps
import Data_Process as dp
#==================CUSTOM IMPORT==================

#Init
def Init_TCU():
    #global GPIO
    global client_Socket, cTt_Ser, data_to_CCU, data_from_CCU, HOST, PORT
    global remote_Active, debug_mode, mode_change_input, wheel_value, warning_LV
    global gps_Ser, latitude, longitude
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
    
    # . Init GPS
    gps_Ser = wcom.Init_UART(port="/dev/ttyAMA1") #GPS Serial
    gps.Threading_GPS(gps_Ser)
    
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
        latitude, longitude = gps.Get_GPS_Datas()
        latitude = int(latitude * 10000)
        longitude = int(longitude * 10000)
        
        # . Setting Datas To Center
        data_set = dp.Trans_Str_To_Arr(data_from_CCU)
        data_set.append(latitude)
        data_set.append(longitude)
        data_to_Center = dp.Trans_Arr_To_Str(data_set)
        wlcom.Send_Socket(client_Socket, data_to_Center)
        
        # . Getting Datas From Center
        data_from_Center = wlcom.Receive_Socket(client_Socket).decode()
        
        center_datas = dp.Trans_Str_To_Arr(data_from_Center)
        warning_LV = dp.Trans_Str_To_Arr(data_from_CCU)
        
        if len(center_datas) == 3:
            if center_datas[0] == 4:
                remote_Active = True
            elif center_datas[0] == 2:
                remote_Active = False
            wheel_value = [center_datas[1], center_datas[2]]

        if remote_Active:
            data_set = [4, wheel_value[0], wheel_value[1]]
            data_to_CCU = dp.Trans_Arr_To_Str(data_set)
            wcom.Send_Data(cTt_Ser, data_to_CCU)
        else:
            data_set = [2, 1500, 0]
            data_to_CCU = dp.Trans_Arr_To_Str(data_set)
            wcom.Send_Data(cTt_Ser, data_to_CCU)
            
        time.sleep(0.05)
        
except Exception as e:
    print("Error! :",e)
    wlcom.Close_Socket(client_Socket)
    #strm.Stop_UV4L_Service()
    print("END")
    
finally:
    
    print("CLEAN")
