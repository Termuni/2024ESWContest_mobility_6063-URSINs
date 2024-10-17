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
    PORT = 9091  #
    client_Socket = wlcom.Init_Client_Socket(HOST, PORT)
    cTt_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    data_to_CCU = "0,0"
    data_from_CCU = '0'
    print("COMPLETE COM")
    
    # . Init GPS
    #gps_Ser = wcom.Init_UART(port="/dev/ttyAMA1") #GPS Serial
    #gps.Threading_GPS(gps_Ser)
    
    # 3. SET extra Datas
    remote_Active = False
    debug_mode = False
    mode_change_input = False
    warning_LV = 0
    wheel_value = [0, 0]


#====================Main==================

try:
    #초기 설정
    print("start")
    Init_TCU()
    time_start = time.time() #Test241011
    data_set = [1] #Test241011
    print("ACTIVE PROCESSING")
    
    
    while True:
        
        data_from_CCU = wcom.Receive_Data(cTt_Ser) # CCU한테 UART 데이터 받음 (응급레벨 <ex."0">)
        cTt_Ser.reset_input_buffer() # UART 버퍼 초기화
        time.sleep(0.01)# 타임 슬립 왜 있지?
        latitude, longitude = gps.Get_GPS_Datas() # GPS 위도,경도 가져옴. (쓰레드로 계속 업데이트 되고 있음)
        latitude = int(latitude * 10000)          # GPS 위도,경도를 int로 만들어서, 원격센터로 보낼 준비.
        longitude = int(longitude * 10000)
        time_now = time.time() #Test241011
        
        # ===[ 원격센터로 데이터 보내기 ]===
        data_set = dp.Trans_Str_To_Arr(data_from_CCU)    # CCU한테 온 데이터를 정제
        #if time_now - time_start <= 10 :
        #    data_set = [1]
        #if time_now - time_start > 10 : #Test241011
        #    data_set = [2]
        #if time_now - time_start > 20 : #Test241011
        #    data_set = [3]
            
        if data_set == [3]: # 응급레벨 3 없애기.
            data_set = [2] # (CCU한테 3 와도, 2로 보내기)
            
        data_set.append(latitude)                        # 데이터에 위도 추가
        data_set.append(longitude)                       # 데이터에 경도 추가
        data_to_Center = dp.Trans_Arr_To_Str(data_set)   # 데이터 정제 (리스트 -> 문자열) 
        wlcom.Send_Socket(client_Socket, data_to_Center) # 원격센터에 데이터 보내기 [응급레벨, 위도, 경도]
        
        # ===[ 원격센터에서 데이터 받기 ]===
        data_from_Center = wlcom.Receive_Socket(client_Socket).decode() # 원격센터에서 데이터 가져옴
        center_datas = dp.Trans_Str_To_Arr(data_from_Center)            # 데이터 정제 (문자열 -> 리스트)
        warning_LV = dp.Trans_Str_To_Arr(data_from_CCU)                 # 응급레벨 = CCU가 보낸 데이터

        if len(center_datas) == 3:                               # 원격센터발 데이터 개수가 3개일 때 :   (ex. [0, 0, 0,])
            if center_datas[0] == 4:                               # 1st 데이터가 4일때 :
                remote_Active = True                                 # 원격운전 실행
            elif center_datas[0] == 2:                             # 1st 데이터가 2일때 : 
                remote_Active = False                                # 원격운전 취소
            wheel_value = [center_datas[1], center_datas[2]]       # 원격운전 데이터 = 2rd, 3th 데이터

        if remote_Active:                                        # 원격운전일 때 :
            wheel_value[0] = int(1500 + ((wheel_value[0] - 1500)*1.5)) # 241014 Test_PHK
            if wheel_value[0] < 0 :
                wheel_value[0] = 0
            data_set = [4, wheel_value[0], wheel_value[1]]         # CCU로 보낼 데이터 준비. [4, 핸들값, 페달값]
            data_to_CCU = dp.Trans_Arr_To_Str(data_set)            # 데이터 정제 (리스트 -> 문자열)
            wcom.Send_Data(cTt_Ser, data_to_CCU)                   # CCU로 데이터(UART) 보냄.
            
        else:                                                    # 원격운전 아닐 때 :
            data_set = [2, 1500, 0]                                # CCU로 보낼 데이터 준비. [2, 1500, 0] (기본값)
            data_to_CCU = dp.Trans_Arr_To_Str(data_set)            # 데이터 정제 (리스트 -> 문자열)
            wcom.Send_Data(cTt_Ser, data_to_CCU)                   # CCU로 데이터(UART) 보냄.
            
        time_stamp = time_now-time_start
        print(f"\n=== <TCU> Time Stamp [{time_stamp}] ===")
        print("Rcv from CCU    :",data_from_CCU)
        print("Sent to Center  :",data_to_Center)
        print("Rcv from Center :", data_from_Center)
        print("Sent  to  CCU   :", data_to_CCU)
        if data_from_Center == '1':
            print("원격센터에서 실내영상 확인 중...")
        else :
            if remote_Active:
                print("원격 운전 중...")
            else:
                print("정상 운전 중...")
            
        time.sleep(0.05)
        
except Exception as e:
    print("Error! :",e)
    wlcom.Close_Socket(client_Socket)
    #strm.Stop_UV4L_Service()
    print("END")
    
finally:
    
    print("CLEAN")
