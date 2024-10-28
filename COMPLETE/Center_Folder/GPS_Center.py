import folium
import os
import time
import webview
import threading
import subprocess

# 지도 파일 경로
global map_file
map_file = 'map.html'

global latitude, longitude
latitude = 37.5665
longitude = 126.9780

# 지도 업데이트 함수
def Update_Map(lat, lon):
    mymap = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup=f'Location: {lat}, {lon}').add_to(mymap)
    mymap.save(map_file)

# 좌표가 변화하는 지도와 함께 실행하는 함수
def Window_GPS():
    # 초기 지도 생성
    Update_Map(37.5665, 126.9780)
    map_file = 'map.html'
    # PyWebView 창 생성
    window = webview.create_window('GPS Map Viewer', 'file://' + os.path.realpath(map_file))
    # 지도 갱신 작업을 스케줄링하는 함수 (window 인자를 받음)
    def Update_Coordinates(window):
        map_file = 'map.html'
        Update_Map(latitude, longitude)  # 지도를 갱신
        window.load_url('file://' + os.path.realpath(map_file))
    
    # PyWebView 이벤트 루프에서 지도 업데이트 실행
    webview.start(Update_Coordinates, window)
    return window

# 지도 갱신 작업을 스케줄링하는 함수 (window 인자를 받음)
def Update_Coordinates(latitude, longitude, window):
    map_file = 'map.html'
    Update_Map(latitude, longitude)  # 지도를 갱신
    window.load_url('file://' + os.path.realpath(map_file))
    



def Threading_GPS():
    thread_gps = threading.Thread(
        target= Window_GPS,
        args=()
    )
    thread_gps.start()


def Set_Gps_Lat_Lon(lat, lon):
    global latitude, longitude
    latitude = lat
    longitude = lon
    
