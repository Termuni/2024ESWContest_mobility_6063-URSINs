import sys, os
import time

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import RC_Wheel as wheel
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU
    global wheel_value, warning_LV
    
    # . Init Communication
    server_Socket = wlcom.Init_Server_Socket()
    data_to_TCU = "Test"
    data_from_TCU = None
    
    # . Init Racing_Wheel
    wheel.Init_Get_Wheel_Value()
    
    # . SET extra Datas
    wheel_value = [0, 0]
    warning_LV = 0
    

#====================Main==================

try:
    #INIT VALUES
    Init_Rmt_Center()
    print("ACTIVE PROCESS")
    
    while True:
        data_from_TCU = wlcom.Receive_Socket(server_Socket).decode()
        if data_from_TCU != '':
            warning_LV = int(data_from_TCU)
        
        print("IN PROCESSING")
        #If Warning LV 2 Received
        if warning_LV == 2:
            print("WARNING : Driver is danger in now")
            #Show Inside CAM
        
        
        #If Warning LV 3 Received
        elif warning_LV == 3:
            print("REMOTE CONTROL ACTIVATE")
        
            #Show Front CAM
        
            #Sending Handle Data
            wheel_value = wheel.Get_Racing_Wheel_Value()
            data_to_TCU = f'{wheel_value[0]},{wheel_value[1]}'
            wlcom.Send_Socket(server_Socket, data_to_TCU)
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    wlcom.Close_Socket(server_Socket)
    print("END")