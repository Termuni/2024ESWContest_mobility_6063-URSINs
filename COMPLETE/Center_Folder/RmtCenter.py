import sys, os
import time
import subprocess
import threading

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import UART_Communication as wcom
import RC_Wheel as wheel
import Streaming as strm
import Rmt_Window as wind
import Data_Process as dp
import GPS_Center as gps
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU, data_to_SubCenter
    global cTs_Ser
    global wheel_value, warning_LV
    global window_active_lv2, window_active_lv3, is_streaming_lv2, is_streaming_lv3
    global streaming_url_lv2, vd_cap_lv2, streaming_url_lv3, vd_cap_lv3
    global latitude, longitude, window_gps
    global TCU_IP, TCU_PORT_Lv2CAM
    TCU_IP = '10.211.173.3'
    TCU_PORT_Lv2CAM = 5000

    # . Init Communication
    server_Socket = wlcom.Init_Server_Socket()
    cTs_Ser = wcom.Init_UART()
    data_to_TCU = "0"
    data_from_TCU = None
    
    # . Init Racing_Wheel
    wheel.Init_Wheel()
    wheel.Init_Get_Wheel_Value()
    
    # . Init Window Flag
    window_active_lv2 = False
    window_active_lv3 = False
    is_streaming_lv2 = False
    is_streaming_lv3 = False
    
    # . Init Streaming
    #streaming_ppl_lv2 = strm.Get_Streaming_Pipeline('192.168.0.5', 5000)
    #vd_cap_lv2 = strm.Get_VideoCapture_Variable(streaming_ppl_lv2)
    
    #streaming_ppl_lv3 = strm.Get_Streaming_Pipeline('192.168.0.5', 9090)
    #vd_cap_lv3 = strm.Get_VideoCapture_Variable(streaming_ppl_lv3)
    
    # . Init GPS
    #gps.Threading_GPS()
    #[latitude, longitude] = [37.5665, 126.9780]
    print("line Test Gps1...")
    #window_gps=gps.Window_GPS()
    # . SET extra Datas
    wheel_value = [0, 0]
    #print("line Test Gps2...")
    warning_LV = 0
    
    

#====================Main==================

try:
    #초기 설정
    Init_Rmt_Center()
    time_start = time.time()
    print("ACTIVE PROCESS")
    #i = 0
    while True:
        #i+=1
        data_from_TCU = wlcom.Receive_Socket(server_Socket).decode()   #TCU한테 온 데이터 [응급레벨, 위도, 경도] 
        tcu_datas = dp.Trans_Str_To_Arr(data_from_TCU)                 #데이터 정제 (문자열 -> 리스트)
        data_to_SubCenter = data_from_TCU
        
        time.sleep(0.01)
        time_now = time.time()
        
        warning_LV = tcu_datas[0]                        # 응급레벨 = 데이터[0]
        if len(tcu_datas) == 3:                          # TCU발 데이터가 3개일 때 (정상일때):
            latitude = tcu_datas[1]/10000                # 위도 정제 (371270 -> 37.1270)
            longitude = tcu_datas[2]/10000               # 경도 정제 (1263290 -> 126.3290)
            #gps.Update_Coordinates(latitude,longitude,window_gps)
            gps.Set_Gps_Lat_Lon(latitude, longitude)     # GPS쓰레드로 위도경도 보내기.

        wheel_value = wheel.Get_Racing_Wheel_Value()     # 레이싱휠 값 [핸들, 페달] 가져오기
        
        
        if warning_LV == 2:                              #=== [ 응급레벨 2일때 ]===
            if wind.Get_LV2_Window_State():                      # 윈도우가 없을 때 (중복 방지)
                wind.Show_Window('Lv2')                      # 레벨2 UI 켜기. 
            print("[WARNING] Driver is danger in now")
        
        if wind.Get_Monitoring_Driver_State():          #===[ 운전자 모니터링 버튼 눌렀을때 ]===
            wind.Set_Monitoring_Driver_Deactivate()        # 운전자 모니터링 상태 False로.
            #Show Inside CAM
            data_to_TCU = "1"
            if not is_streaming_lv2:
                streaming_ppl_lv2 = strm.Get_Streaming_Pipeline(TCU_IP, TCU_PORT_Lv2CAM)
                vd_cap_lv2 = strm.Get_VideoCapture_Variable(streaming_ppl_lv2)
            strm.Thread_Streaming(vd_cap_lv2)              # 내부캠 영상 보기.        
            wind.Show_Window('Remote_Select')              # 원격운전 실행 UI 켜기.
            is_streaming_lv2 = True                        # 레벨2 스트리밍 트리거 = True


        
        if wind.Get_Remote_Forced_State() == 1:         #===[ 레벨2에서, 긴급원격운전 버튼 눌렀을때 ]===
            wind.Set_Remote_Forced_Default()              # 긴급운전 상태 = 0 (기본값)
            warning_LV = 3                                # 응급레벨 3으로 만들기
            window_active_lv3 = True                      # 레벨3 트리거 = True
            wind.Set_Remote_Drive_Activate()              # 원격운전 트리거 = True
        
        #If Warning LV 3 Received
        if warning_LV == 3:                             #===[ 응급레벨 3일 때: ]===
            if not window_active_lv3:                     # 레벨3 트리거가 없을 때 (원격센터에서 만든 레벨3가 아닐 때:) 
                wind.Show_Window('Lv3')                   # 레벨3 UI 켜기
                window_active_lv3 = True                  # 레벨3 트리거 = True
            print("REMOTE CONTROL ACTIVATE")
        
        if wind.Get_Remote_Drive_State():               # 원격운전 트리거 True 일때 :
            wind.Set_Remote_Drive_Deactivate()          # 원격운전 트리거 = False
            #Show Front CAM
            #streaming_ppl_lv3 = strm.Get_Streaming_Pipeline('192.168.0.5', 9090)
            #vd_cap_lv3 = strm.Get_VideoCapture_Variable(streaming_ppl_lv3)
            vid_thread = threading.Thread(target = strm.Run_New_Term, args=()) # 외부캠 쓰레딩 설정 
            vid_thread.start()                          # 외부캠 영상 보기
            is_streaming_lv3 = True                     # 레벨3 스트리밍 트리거 = True
        
        
        if is_streaming_lv3:                            # 레벨3 스트리밍 트리거 True 일때 :
            #Sending Handle Data
            if wind.Get_Remote_Forced_State() == 2:     # 강제운전 트리거 = 2 일때
                data_set = [2]
            else:                                       # 강제운전 상태 = 0 or 1 일때
                data_set = [4]                          # 원격운전
            #data_set.append(wheel_value)                # 레이싱휠값 [핸들, 페달]
            data_set.append(int(wheel_value[0]))
            data_set.append(int(wheel_value[1])) 
            data_to_TCU = dp.Trans_Arr_To_Str(data_set) # TCU로 보낼 데이터 정제
        
        
        #Data to SubCenter and TCU
        wcom.Send_Data(cTs_Ser, data_to_SubCenter)
        wlcom.Send_Socket(server_Socket, data_to_TCU)   # TCU로 데이터 보냄.
        
        
        time_stamp = time_now-time_start
        print(f"\n=== <RmtCenter>ltw1 Time Stamp [{time_stamp}] ===")
        print("Rcv from TCU :",tcu_datas)
        print("Send to TCU  :",data_to_TCU)
        
        time.sleep(0.05)
        
except KeyboardInterrupt:
    wlcom.Close_Socket(server_Socket)
    print("END")
