#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(__path__)))

#==================CUSTOM IMPORT==================
from ACPE import ACPE as acpe
from HeartBeat import BPM as bpm
#==================CUSTOM IMPORT==================

#Set Constant Values

def Init():
    
    bpm.Init_BPM()

#====================Main(START)==================

if __name__ == "__main__":

    try:
        #INIT VALUES
        #Set Class
        
        print("START PROCESSING")
        while True:
            #If Debug Mode
            print("DEBUG MODE ACTIVATE")
            
            #Else Getting Sensor Value
            print("DEBUG MODE DEACTIVATE")
            bpm.Get_BPM_Data()                  #What You can use : bpm.ppg_avg_bpm / bpm_ecg_avg_bpm
            
            #Warning Lv Calculate By Algorithm
            
            
            #If Warning LV 1
                #LCD Alarm
                #Remote Off
            
            
            #Elif Warning LV 2
                #Sound Output
                #LED ON
                #Remote Off
            
            
            #Elif Warning LV 3
                #Remote On
            
            
            #If Remote OFF
                #Set Motor Data by CCU
            
            
            #Else Remote ON
                #Get Motor Data from TCU
            
            
            #If There Is Nothing Blocking Front
                #Sending Motor and Submotor Value
            
            
            #Else Something Blocking Front
            print("ACPE ACTIVE")
            
    except:
        print("END")
        
    finally:
        print("CLEAN")

#====================Main(END)==================