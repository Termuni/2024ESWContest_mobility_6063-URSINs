import sys, os
import time
import subprocess
import threading

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import RC_Wheel as wheel
import Streaming as strm
import Rmt_Window as wind
import Data_Process as dp
import GPS_Center as gps
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU
    global wheel_value, warning_LV
    global window_active_lv2, window_active_lv3, is_streaming_lv2, is_streaming_lv3
    global streaming_url_lv2, vd_cap_lv2, streaming_url_lv3, vd_cap_lv3
    global latitude, longitude, window_gps
    
    # . Init Communication
    HOST = '0.0.0.0'
    PORT = 9092
    server_Socket=wlcom.Init_Server_Socket(HOST, PORT)
    print('Server listening...')
    #s.setblocking(False)



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
    [latitude, longitude] = [37.5665, 126.9780]

    # . SET extra Datas
    wheel_value = [0, 0]
    warning_LV = 0
    
    

import serial
import folium
import os
import time
import webview

# 지도 파일 경로
map_file = 'map.html'
# 지도 업데이트 함수
def update_map(lat, lon):
    mymap = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup=f'Location: {lat}, {lon}').add_to(mymap)
    mymap.save(map_file)
    
def get_gps_data():
    data_from_TCU = wlcom.Receive_Socket(server_Socket).decode()   #TCU한테 온 데이터 [응급레벨, 위도, 경도]
    print(data_from_TCU)
    tcu_datas = dp.Trans_Str_To_Arr(data_from_TCU)                 #데이터 정제 (문자열 -> 리스트)
    latitude = tcu_datas[0]/10000
    longitude = tcu_datas[1]/10000
    return latitude, longitude

# 좌표가 변화하는 지도와 함께 실행하는 함수
def main():
    # 초기 지도 생성
    Init_Rmt_Center()
    latitude, longitude = 37.5665, 126.9780  # 서울 시청을 기본값으로 설정
    update_map(latitude, longitude)
    
    # PyWebView 창 생성
    window = webview.create_window('GPS Map Viewer', 'file://' + os.path.realpath(map_file), width=500, height=400)

    # 지도 갱신 작업을 스케줄링하는 함수 (window 인자를 받음)
    def update_coordinates(window):
        while True:
            latitude, longitude = get_gps_data()  # GPS 데이터를 받아옴
            update_map(latitude, longitude)  # 지도를 갱신
            window.load_url('file://' + os.path.realpath(map_file))
            print("latitude :", latitude)
            print("longitude :", longitude)
            time.sleep(0.5)

    # PyWebView 이벤트 루프에서 지도 업데이트 실행
    webview.start(update_coordinates, window)



#====================Main==================
try: 
    main()
except Exception as e:
    print("Error! :", e)
    wlcom.Close_Socket(server_Socket)
    print("END")
