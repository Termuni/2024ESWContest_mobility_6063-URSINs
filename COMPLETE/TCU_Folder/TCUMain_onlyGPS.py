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
    #HOST = '192.168.0.2'
    PORT = 9092  #
    client_Socket = wlcom.Init_Client_Socket(HOST, PORT)
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
    #초기 설정
    Init_TCU()
    time_start = time.time() #Test241011
    data_set = [1] #Test241011
    print("ACTIVE PROCESSING")
    i = 0
    while True:
        #i += 1
        latitude, longitude = gps.Get_GPS_Datas() # GPS 위도,경도 가져옴. (쓰레드로 계속 업데이트 되고 있음)
        latitude = int(latitude * 10000)# + i        # GPS 위도,경도를 int로 만들어서, 원격센터로 보낼 준비.
        longitude = int(longitude * 10000)# + i
         
        data_set = [latitude, longitude,0]
        data_to_Center = dp.Trans_Arr_To_Str(data_set)   # 데이터 정제 (리스트 -> 문자열) 
        wlcom.Send_Socket(client_Socket, data_to_Center) # 원격센터에 데이터 보내기 [응급레벨, 위도, 경도]
        print("Sent to Center :",data_to_Center)
            
        time.sleep(1)
        
except Exception as e:
    print("Error! :",e)
    wlcom.Close_Socket(client_Socket)
    #strm.Stop_UV4L_Service()
    print("END")
    
finally:
    
    print("CLEAN")
