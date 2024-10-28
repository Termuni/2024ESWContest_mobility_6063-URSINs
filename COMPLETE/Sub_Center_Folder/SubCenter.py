import sys, os
import time
import subprocess
import threading

#==================CUSTOM IMPORT==================
import UART_Communication as wcom
import Streaming as strm
import Data_Process as dp
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global cTs_ser, data_from_Center
    global warning_LV
    global window_active_lv3, is_streaming_lv3
    global streaming_url_lv3, vd_cap_lv3
    global TCU_IP, TCU_PORT_Lv3CAM
    TCU_IP = '10.211.173.3'
    TCU_PORT_Lv3CAM = 9090
    
    # . Init Communication
    data_from_Center = None
    cTs_ser = wcom.Init_UART(port = "/dev/serial0")
    
    # . Init Window Flag
    window_active_lv3 = False
    is_streaming_lv3 = False
    
    # . SET extra Datas
    warning_LV = 0
    

#====================Main==================

try:
    #초기 설정
    Init_Rmt_Center()
    time_start = time.time()
    print("ACTIVE PROCESS")
    
    while True:
        #i+=1
        data_from_Center = wcom.Receive_Data()
        tcu_datas = dp.Trans_Str_To_Arr(data_from_Center)                 #데이터 정제 (문자열 -> 리스트)
        
        time.sleep(0.01)
        
        warning_LV = tcu_datas[0]                        # 응급레벨 = 데이터[0]
        if len(tcu_datas) == 3:                          # TCU발 데이터가 3개일 때 (정상일때):
            latitude = tcu_datas[1]/10000                # 위도 정제 (ex : 371270 -> 37.1270)
            longitude = tcu_datas[2]/10000               # 경도 정제 (ex : 1263290 -> 126.3290)
        
        #If Warning LV 4 Received
        if warning_LV == 4:                             #===[ 응급레벨 3일 때: ]===
            if not window_active_lv3:                   # 레벨3 트리거가 없을 때 (원격센터에서 만든 레벨3가 아닐 때:) 
                window_active_lv3 = True                # 레벨3 트리거 = True
                gps_thread = threading.Thread(          # GPS 실행시키는 Thread 생성
                    target=strm.Run_New_Term)
                # 스레딩 시작
                gps_thread.start()                      # GPS 실행
            print("REMOTE CONTROL ACTIVATE")
        
        if window_active_lv3:                           # 원격운전 트리거 True 일때 :
            #Show Front CAM
            streaming_ppl_lv3 = strm.Get_Streaming_Pipeline('10.211.173.3', 9090)
            vd_cap_lv3 = strm.Get_VideoCapture_Variable(streaming_ppl_lv3)
            strm.Get_Streaming(vd_cap_lv3)              # 여기서 무한 루프 돌면서 영상 보여줌
            window_active_lv3 = False                   # 레벨3 스트리밍 트리거 = True
        
        time_now = time.time()
        
        time_stamp = time_now-time_start
        print(f"\n=== <RmtCenter>ltw1 Time Stamp [{time_stamp}] ===")
        print("Rcv from TCU :",tcu_datas)
        time.sleep(0.05)
        
except KeyboardInterrupt:
    
    print("END")
