
import sys, os
import time

#==================CUSTOM IMPORT==================
import TCP_IP_Communication as wlcom
import UDAS as udas
#==================CUSTOM IMPORT==================

def Init_Rmt_Center():
    global server_Socket, data_to_TCU, wheel_value
    
    # 1. Init Communication
    
    # 2. SET extra Datas
    

#====================Main==================

try:
    #INIT VALUES
    Init_Rmt_Center()
    print("ACTIVE PROCESS")
    
    while True:
        print("IN PROCESSING")
        #If Warning LV 2 Received
        
            #Show Inside CAM
        
        
        #If Warning LV 3 Received
        
            #Show Front CAM
        
            #Sending Handle Data
        
        
        
        
        print("")
except:
    print("END")