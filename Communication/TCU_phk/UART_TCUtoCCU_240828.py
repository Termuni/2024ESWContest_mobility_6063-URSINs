# DMU(젯슨나노)에서 CCU로 보낼 UART 통신 코드
# 박현규. 240828


import serial
from time import sleep

ser = serial.Serial("/dev/ttyUSB0", 9600) #Open port with baud ratese

while True:
    received_data = ser.read() #read serial port
    sleep(0.3)
    data_left = ser.inWaiting() #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data) #print received data
    ser.write(received_data) #transmit data serially
