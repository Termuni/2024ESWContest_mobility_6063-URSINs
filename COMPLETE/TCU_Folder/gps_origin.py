import serial
import folium
import os
import time
import webview

# 시리얼 포트 설정 (라즈베리파이의 UART 포트 /dev/serial0 또는 /dev/ttyUSB0)
gps = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# 지도 파일 경로
map_file = 'map.html'

# NMEA 데이터를 십진수 도(DD)로 변환하는 함수
def nmea_to_decimal(degrees_minutes, direction):
    # 도 부분과 분 부분을 정확히 분리
    if degrees_minutes[5] == '.':  # 경도일 경우 (3자리 도)
        degrees = int(degrees_minutes[:3])  # 경도에서 3자리 도 부분 추출
        minutes = float(degrees_minutes[3:])  # 나머지 부분은 분으로 추출
    else:  # 위도일 경우 (2자리 도)
        degrees = int(degrees_minutes[:2])  # 위도에서 2자리 도 부분 추출
        minutes = float(degrees_minutes[2:])  # 나머지 부분은 분으로 추출
    
    # 분을 도로 변환
    decimal_degrees = degrees + (minutes / 60)
    
    # 남(S) 또는 서(W)일 경우 음수로 변환
    if direction == 'S' or direction == 'W':
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees


# GPS에서 위치 정보를 받아 지도에 업데이트하는 함수
def get_gps_data():
    while True:
        data = gps.readline().decode('utf-8', errors='replace')
        if data.startswith('$GPRMC'):  # GPRMC 데이터 사용
            gprmc_fields = data.split(',')
            if gprmc_fields[2] == 'A':  # 수신 상태가 유효한 경우에만 처리
                latitude = gprmc_fields[3]  # 위도
                latitude_direction = gprmc_fields[4]  # N 또는 S
                longitude = gprmc_fields[5]  # 경도
                longitude_direction = gprmc_fields[6]  # E 또는 W
                print(latitude, latitude_direction, longitude, longitude_direction)
                
                
                # 위도, 경도를 십진수 도로 변환
                latitude_decimal = nmea_to_decimal(latitude, latitude_direction)
                longitude_decimal = nmea_to_decimal(longitude, longitude_direction)
                
                print(f'Updated GPS coordinates: Latitude = {latitude_decimal}, Longitude = {longitude_decimal}')
                return latitude_decimal, longitude_decimal

# 지도 업데이트 함수
def update_map(lat, lon):
    mymap = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup=f'Location: {lat}, {lon}').add_to(mymap)
    mymap.save(map_file)

# 좌표가 변화하는 지도와 함께 실행하는 함수
def main():
    # 초기 지도 생성
    latitude, longitude = 37.5665, 126.9780  # 서울 시청을 기본값으로 설정
    update_map(latitude, longitude)

    # PyWebView 창 생성
    window = webview.create_window('GPS Map Viewer', 'file://' + os.path.realpath(map_file))

    # 지도 갱신 작업을 스케줄링하는 함수 (window 인자를 받음)
    def update_coordinates(window):
        while True:
            latitude, longitude = get_gps_data()  # GPS 데이터를 받아옴
            update_map(latitude, longitude)  # 지도를 갱신
            window.load_url('file://' + os.path.realpath(map_file))
            time.sleep(1)

    # PyWebView 이벤트 루프에서 지도 업데이트 실행
    webview.start(update_coordinates, window)

if __name__ == "__main__":
    main()

