
# 시리얼 포트 설정 (라즈베리파이의 UART 포트 /dev/serial0 또는 /dev/ttyUSB0)
# gps = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

import threading


global latitude, longitude

[latitude, longitude] = [37.5665, 126.9780]

# 지도 파일 경로
map_file = 'map.html'

# NMEA 데이터를 십진수 도(DD)로 변환하는 함수
def NMEA_To_Dec(degrees_minutes, direction):
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
def Return_GPS_Data(gps):
    while True:
        data = gps.readline().decode('utf-8', errors='replace')
        if data.startswith('$GPRMC'):  # GPRMC 데이터 사용
            gprmc_fields = data.split(',')
            if gprmc_fields[2] == 'A':  # 수신 상태가 유효한 경우에만 처리
                latitude = gprmc_fields[3]  # 위도
                latitude_direction = gprmc_fields[4]  # N 또는 S
                longitude = gprmc_fields[5]  # 경도
                longitude_direction = gprmc_fields[6]  # E 또는 W
                
                # 위도, 경도를 십진수 도로 변환
                latitude_dec = NMEA_To_Dec(latitude, latitude_direction)
                longitude_dec = NMEA_To_Dec(longitude, longitude_direction)
                return latitude_dec, longitude_dec
 
def Update_GPS_Data(gps):
    global latitude, longitude
    try:
        while True:
            latitude, longitude = Return_GPS_Data(gps)
    except KeyboardInterrupt:
        print("STOP GPS")
    
def Threading_GPS(gps):
    thread_gps = threading.Thread(target= Update_GPS_Data, args=(gps,))
    thread_gps.start()
    
    
def Get_GPS_Datas():
    global latitude, longitude
    return latitude, longitude