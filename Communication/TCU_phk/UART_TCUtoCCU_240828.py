# DMU(��������)���� CCU�� ���� UART ��� �ڵ�
# ������. 240828


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
