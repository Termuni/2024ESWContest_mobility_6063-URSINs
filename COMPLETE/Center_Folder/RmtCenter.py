import sys, os
import time

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import RC_Wheel as wheel
import Streaming as strm
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU
    global wheel_value, warning_LV
    global streaming_url_lv2, vd_cap_lv2, streaming_url_lv3, vd_cap_lv3
    
    # . Init Communication
    server_Socket = wlcom.Init_Server_Socket()
    data_to_TCU = "Test"
    data_from_TCU = None
    
    # . Init Racing_Wheel
    wheel.Init_Wheel()
    wheel.Init_Get_Wheel_Value()
    
    # . Init Streaming
    streaming_url_lv2 = strm.Get_Streaming_URL(8080)
    vd_cap_lv2 = strm.Get_VideoCapture_Variable(streaming_url_lv2)
    streaming_url_lv3 = strm.Get_Streaming_URL(9090)
    vd_cap_lv3 = strm.Get_VideoCapture_Variable(streaming_url_lv3)
    
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
        wlcom.Send_Socket(server_Socket, data_to_TCU)
        if data_from_TCU != '':
            warning_LV = int(data_from_TCU)
            
        print(f'{data_from_TCU}, {warning_LV}')
        
        #If Warning LV 2 Received
        if warning_LV == 2:
            print("WARNING : Driver is danger in now")
            #Show Inside CAM
            strm.Thread_Streaming(vd_cap_lv2)
        
        
        #If Warning LV 3 Received
        elif warning_LV == 3:
            print("REMOTE CONTROL ACTIVATE")
        
            #Show Front CAM
            strm.Thread_Streaming(vd_cap_lv3)
        
            #Sending Handle Data
            wheel_value = wheel.Get_Racing_Wheel_Value()
            data_to_TCU = f'{wheel_value[0]},{wheel_value[1]}'
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    wlcom.Close_Socket(server_Socket)
    print("END")