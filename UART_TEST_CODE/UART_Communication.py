"""
[UART통신 규칙] - 2024.09.19 현규 작성
1. Raspberry Pi Configuration - Interfaces - Serial Console >> 비활성화(Disable)
2. sudo apt-get install python3-serial
3. 한쪽의 Tx핀은, 다른 RPi의 Rx핀과 연결되어야함.  (Rx <-> Tx,   Tx <-> Rx)
4. 송신할 Data가 없을 경우, 'None'이 아닌 '0'을 송신해야함. 
5. 모든 Data는, 마지막에 '\n'으로 줄바꿈을 해서 마무리해야함.
6. DMU-CCU 연결부의 CCU에서, DMU의 Tx는 CCU의 GPIO 5(Rx),  DMU의 RX는 CCU의 GPIO 4에 연결해야함.
"""

import serial
import time

def Init_UART(port="/dev/serial0", baudrate=9600):
    """
    CCU, DMU, TCU에서 사용.
    RPi의 기본 시리얼포트.
    
    UART 포트를 초기화합니다.
    :param port: UART 포트 경로 (예: /dev/serial0)
    :param baudrate: 통신 속도, 보드레이트 (예: 9600)
    :return: 초기화된 serial 객체를 반환
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser


def Send_Data(ser, data = '0'):
    """
    데이터를 UART를 통해 전송합니다.
    데이터가 없을 경우 '0'을 전송합니다.
    :param ser: 초기화된 serial 객체
    :param data: 전송할 문자열 데이터 (None이면 '0'을 전송)
    """
    if isinstance(ser, serial.Serial):
        ser.write(data.encode('utf-8'))  # 데이터를 바이트 형태로 인코딩하여 전송
        print(f"Sent: {data}")  # 전송된 데이터 출력
    else:
        print(f"{ser} is not Serial!")


def Receive_Data(ser):
    """
    [CCU, TCU에서 사용.]
    UART를 통해 데이터를 수신합니다.
    :param ser: 초기화된 serial 객체
    :return: 수신된 문자열 데이터 (없으면 '0'을 반환)
    """
    if isinstance(ser, serial.Serial):
        if ser.in_waiting > 0:  # 수신된 데이터가 있는지 확인
            data = ser.readline().decode('utf-8').strip()  # 수신된 데이터를 문자열로 디코딩
            if data:
                print(f"Received: {data}")  # 수신된 데이터 출력
                return data
    print(f"{ser} is not Serial!")
    return '0'


def Receive_Data_DMU(ser):
    """
    UART를 통해 데이터를 수신합니다.
    수신된 데이터가 없을 경우 '0'을 반환합니다.
    :param ser: 초기화된 serial 객체
    :return: 수신된 문자열 데이터 (없으면 '0'을 반환)
    """
    if ser.in_waiting > 0:  # 수신된 데이터가 있는지 확인
        data = ser.readline().decode('utf-8').strip()  # 수신된 데이터를 문자열로 디코딩
        #data = ser.read(5).decode('utf-8').strip()
        #data = ser.readline() # 수신된 데이터를 문자열로 디코딩
        print(data)
        if data:
            print(f"Received: {data}")  # 수신된 데이터 출력
            return data
    return '0'  # 데이터가 없으면 '0' 반환




def Close_UART(ser):
    """
    UART 포트를 닫습니다.
    :param ser: 초기화된 serial 객체
    """
    if isinstance(ser, serial.Serial):
        ser.close()


def Master_COM(ser, data=None):
    """
    마스터 장치에서 데이터를 전송하고 응답을 수신합니다.
    :param ser: 초기화된 serial 객체
    :param data: 전송할 문자열 데이터 (None이면 '0'을 전송)
    :return: 슬레이브로부터 수신된 응답 데이터
    """
    if isinstance(ser, serial.Serial):
        Send_Data(ser, data)  # 데이터 전송
        response = Receive_Data(ser)  # 슬레이브의 응답 수신
        return response
    else:
        print(f"{ser} is not Serial!")

def Slave_COM(ser, data=None):
    """
    슬레이브 장치에서 데이터를 수신하고 응답을 전송합니다.
    :param ser: 초기화된 serial 객체
    :param data: 응답할 문자열 데이터 (None이면 '0'을 전송)
    :return: 마스터로부터 수신된 메시지
    """
    if isinstance(ser, serial.Serial):
        message = Receive_Data(ser)  # 마스터로부터 메시지 수신
        Send_Data(ser, data)  # 응답 데이터 전송
        return message
    else:
        print(f"{ser} is not Serial!")
