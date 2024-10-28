import sys, os
import time
import subprocess
import threading
import serial
import folium
import os
import time
import webview


def Init_Rmt_Center():
    global latitude, longitude, window_gps
    [latitude, longitude] = [37.5768, 126.8981]

# 지도 파일 경로
map_file = 'map.html'
# 지도 업데이트 함수
def update_map(lat, lon):
    mymap = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup=f'Location: {lat}, {lon}').add_to(mymap)
    mymap.save(map_file)
    
def get_gps_data():
    global latitude, longitude
    return latitude, longitude

# 좌표가 변화하는 지도와 함께 실행하는 함수
def main():
    global latitude, longitude
    # 초기 지도 생성
    Init_Rmt_Center()
    
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
    print("END")
