'''
각 센서 별 판단 레벨에 가중치를 반영하여 최종 스코어 및 레벨을 산출하는 알고리즘 코드
HR: Heart Rate
DC: Driver Camera
'''

import RPi.GPIO as GPIO
import time
import smbus

# GPIO 핀 설정
HR_PIN = 17
DC_PIN = 18
I2C_BUS = 1
EEPROM_ADDRESS = 0x50

def Read_Byte_Eeprom(address):
    '''
    EEPROM에서 단일 바이트를 읽는 함수
    address: EEPROM의 메모리 주소
    '''
    address_high = (address >> 8) & 0xFF
    address_low = address & 0xFF
    bus.write_i2c_block_data(EEPROM_ADDRESS, address_high, [address_low])
    time.sleep(0.05)
    data = bus.read_byte(EEPROM_ADDRESS)
    return data

def Read_Data_Eeprom(start_address, num_bytes):
    '''
    EEPROM에서 여러 바이트를 읽는 함수
    start_address: EEPROM의 메모리 시작 주소
    num_bytes: 읽을 바이트 수
    '''
    data = []
    for i in range(num_bytes):
        data.append(Read_Byte_Eeprom(start_address + i))
    return data

#Leveling Algorithm 초기 설정
def Initiate_Level_Algorithm():

   # 이거 이렇게 하는 거 맞나 확인 필요..
   global weights, sensor_periods, next_read_time, bus, hr_data

   # GPIO 모드 설정
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(HR_PIN, GPIO.IN)
   GPIO.setup(DC_PIN, GPIO.IN)
   
   # 가중치 설정
   weights = {
       'HR': 0.3,
       'DC': 0.5,
   }
   
   # 각 센서의 데이터 수집 주기
   sensor_periods = {
       'HR': 0.5,  # Heart Rate: 1초마다
       'DC': 1.0, # Eye Blink Rate: 0.5초마다
   }

	# 각 센서의 다음 수집 시간 초기화
   next_read_time = {
       'HR': time.time(),
       'DC': time.time(),
	}
	
	# EEPROM 사용을 위한 설정 초기화 (EEPROM_ADDRESS는 레퍼런스를 참고하여 수정 필요)
  # 60 / 75 / 90 으로 등록
	bus = smbus2.SMBus(I2C_BUS)
	hr_data = Read_Data_Eeprom(0x50, 3)

# Heart Rate 레벨을 정의하는 함수
def Get_Hr_Level(hr_value):
    if hr_value < hr_data[0]:
        return 0  # 정상
    elif hr_data[0] <= hr_value < hr_data[1]:
        return 1  # 주의
    elif hr_data[1] <= hr_value < hr_data[2]:
        return 2  # 경고
    else:
        return 3  # 위험

# Driver Camera 레벨을 정의하는 함수
def Get_Dc_level(dc_value):
    if dc_value < 50:
        return 0  # 정상
    elif 50 <= dc_value < 75:
        return 1  # 주의
    elif 75 <= dc_value < 90:
        return 2  # 경고
    else:
        return 3  # 위험

# 가중 합계 계산 함수
def Calculate_Weighted_Score(sensor_data, weights):
    weighted_score = 0
    for sensor, value in sensor_data.items():
        weighted_score += value * weights[sensor]
    return weighted_score

# 운전자 상태 평가 함수
def Evaluate_Driver_State(weighted_score):
    if weighted_score < 0.5:
        return 0  # 정상
    elif 0.5 <= weighted_score < 1.5:
        return 1  # 주의
    elif 1.5 <= weighted_score < 2.5:
        return 2  # 경고
    else:
        return 3  # 위험

# 초기 설정 
Initiate_Level_Algorithm()

try:
    while True:
        current_time = time.time()
        sensor_data = {}

        # 각 센서의 데이터를 주기에 맞춰 읽기
        if current_time >= next_read_time['HR']:
            hr_value = GPIO.input(HR_PIN)
            sensor_data['HR'] = Get_Hr_Level(hr_value)
            next_read_time['HR'] += sensor_periods['HR']

        if current_time >= next_read_time['DC']:
            dc_value = GPIO.input(DC_PIN)
            sensor_data['DC'] = Get_Dc_Level(dc_value)
            next_read_time['DC'] += sensor_periods['DC']

        # 만약 모든 센서 데이터를 읽었다면
        if sensor_data:
            # 가중치 반영 총 스코어 계산
            weighted_score = Calculate_Weighted_Score(sensor_data, weights)
            # 운전자 상태 평가
            driver_state = Evaluate_Driver_State(weighted_score)

            # 결과 출력
            print("Sensor Data: {}".format(sensor_data))
            print("Weighted Score: {}".format(weighted_score))
            print("Driver State: {}".format(driver_state))

        # CPU 사용률 조절
        time.sleep(0.01)

except KeyboardInterrupt:
    print("프로그램이 중단되었습니다.")
finally:
    GPIO.cleanup()
