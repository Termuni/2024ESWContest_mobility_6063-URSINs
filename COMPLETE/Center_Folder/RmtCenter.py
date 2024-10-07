import sys, os
import time
import subprocess
import threading

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import RC_Wheel as wheel
import Streaming as strm
import Rmt_Window as wind
import Data_Process as dp
import COMPLETE.Center_Folder.GPS_Center as gps
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, data_from_TCU
    global wheel_value, warning_LV
    global window_active_lv2, window_active_lv3, is_streaming_lv2, is_streaming_lv3
    global streaming_url_lv2, vd_cap_lv2, streaming_url_lv3, vd_cap_lv3
    global latitude, longitude
    
    # . Init Communication
    server_Socket = wlcom.Init_Server_Socket()
    data_to_TCU = "0"
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
    streaming_ppl_lv2 = strm.Get_Streaming_Pipeline('10.211.173.3', 5000)
    vd_cap_lv2 = strm.Get_VideoCapture_Variable(streaming_ppl_lv2)
    streaming_ppl_lv3 = strm.Get_Streaming_Pipeline('10.211.173.3', 9090)
    vd_cap_lv3 = strm.Get_VideoCapture_Variable(streaming_ppl_lv3)
    
    # . Init GPS
    gps.Threading_GPS()
    [latitude, longitude] = [37.5665, 126.9780]
    
    # . SET extra Datas
    wheel_value = [0, 0]
    warning_LV = 0
    
    

#====================Main==================

try:
    #INIT VALUES
    Init_Rmt_Center()
    print("ACTIVE PROCESS")
    #i = 0
    while True:
        #i+=1
        data_from_TCU = wlcom.Receive_Socket(server_Socket).decode()
        tcu_datas = dp.Trans_Str_To_Arr(data_from_TCU)
        time.sleep(0.01)
        
        warning_LV = tcu_datas[0]
        if len(tcu_datas) == 3:
            latitude = tcu_datas[1]/10000
            longitude = tcu_datas[2]/10000
            gps.Set_Gps_Lat_Lon(latitude, longitude)

        wheel_value = wheel.Get_Racing_Wheel_Value()
        
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
            wind.Show_Window('Remote_Select')
            is_streaming_lv2 = True
        
        if wind.Get_Remote_Forced_State() == 1:
            wind.Set_Remote_Forced_Default()
            warning_LV = 3
            window_active_lv3 = True
            wind.Set_Remote_Drive_Activate()
        
        #If Warning LV 3 Received
        if warning_LV == 3:
            if not window_active_lv3:
                wind.Show_Window('Lv3')
                window_active_lv3 = True
            print("REMOTE CONTROL ACTIVATE")
        
        if wind.Get_Remote_Drive_State():
            wind.Set_Remote_Drive_Deactivate()
            #Show Front CAM
            vid_thread = threading.Thread(target = strm.Run_New_Term, args=())
            vid_thread.start()
            is_streaming_lv3 = True
        
        if is_streaming_lv3:
            #Sending Handle Data
            if wind.Get_Remote_Forced_State() == 2:
                data_set = [2]
            else:
                data_set = [4]
            data_set.append(wheel_value)
            data_to_TCU = dp.Trans_Arr_To_Str(data_set)
        
        print(data_to_TCU)
        wlcom.Send_Socket(server_Socket, data_to_TCU)
        
        time.sleep(0.05)
        
except KeyboardInterrupt:
    wlcom.Close_Socket(server_Socket)
    print("END")
