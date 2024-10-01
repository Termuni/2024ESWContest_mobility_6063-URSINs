import sys, os
import time

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import RC_Wheel as wheel
import Streaming as strm
import Rmt_Window as wind
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU
    global wheel_value, warning_LV
    global window_active_lv2, window_active_lv3, is_streaming_lv2, is_streaming_lv3
    global streaming_url_lv2, vd_cap_lv2, streaming_url_lv3, vd_cap_lv3
    
    # . Init Communication
    server_Socket = wlcom.Init_Server_Socket()
    data_to_TCU = "Test"
    data_from_TCU = None
    
    # . Init Racing_Wheel
    wheel.Init_Wheel()
    wheel.Init_Get_Wheel_Value()
    
    # . Init Window Flag
    window_active_lv2 = False
    window_active_lv3 = False
    is_streaming_lv2 = False
    is_streaming_lv3 = False
    
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
            if not window_active_lv2:
                wind.Show_Window('Lv2')
                window_active_lv2 = True
            print("WARNING : Driver is danger in now")
        
        if wind.Get_Monitoring_Driver_State():
            wind.Set_Monitoring_Driver_Deactivate()
            #Show Inside CAM
            strm.Thread_Streaming(vd_cap_lv2)
            is_streaming_lv2 = True
        
        
        #If Warning LV 3 Received
        if warning_LV == 3:
            if not window_active_lv3:
                wind.Show_Window('Lv3')
                window_active_lv3 = True
            print("REMOTE CONTROL ACTIVATE")
        
        if wind.Get_Remote_Drive_State():
            wind.Set_Remote_Drive_Deactivate()
            #Show Front CAM
            strm.Thread_Streaming(vd_cap_lv3)
            is_streaming_lv3 = True
        
        if is_streaming_lv3:
            #Sending Handle Data
            wheel_value = wheel.Get_Racing_Wheel_Value()
            data_to_TCU = f'{4},{wheel_value[0]},{wheel_value[1]}'
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    wlcom.Close_Socket(server_Socket)
    print("END")