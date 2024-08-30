#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(__path__)))

#==================CUSTOM IMPORT==================
from ACPE import ACPE as acpe
from HeartBeat import BPM as bpm
import Warning_Score_Calculator as warn
#==================CUSTOM IMPORT==================

#Set Constant Values

def Init_CCU():
    global GPIO, debug_mode, mode_change_input, pedal_error, warning_score
    # 1. SET GPIO
    GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
    
    # 2. Init acpe
    acpe.Init_ACPE()
    
    # 3. Init bpm
    bpm.Init_BPM()
    bpm.Init_Get_BPM_Data()
    
    # 4. SET extra Datas
    debug_mode = False
    mode_change_input = False
    warning_score = 0



#====================Main(START)==================

if __name__ == "__main__":

    try:
        #INIT VALUES
        Init_CCU()
        print("START PROCESSING")
        
        while True:
            # 1. Debug Mode Set
            if mode_change_input:
                debug_mode = not debug_mode
                
                #If Debug Mode
                if debug_mode:
                    print("DEBUG MODE ACTIVATE")

                #Else Getting Sensor Value
                else: 
                    print("DEBUG MODE DEACTIVATE")
                
                
            # 2. Set Values of Racing Wheel --> Is this Right?
            acpe.Communication_With_Remote_Center.Interpret_Packet()
            
            
            # 3. Warning Lv Calculate By Algorithm
            pedal_error = acpe.ACPE_System.Check_Pedal_Error()
            warning_score = warn.Calculate_Warning_Score(bpm.ppg_bpm_level, bpm.ecg_bpm_level, 0, pedal_error, warning_score)
            
            
            # 4. Warning Lv Usage
            
            #If Warning LV 1
            if 50 > warning_score >= 25:
                print("WARNING LV 1")
                #LCD Alarm
                #Remote Off
            
            
            #Elif Warning LV 2
            elif 75 > warning_score >= 50:
                print("WARNING LV 2")
                #Sound Output
                #LED ON
                #Remote Off
            
            
            #Elif Warning LV 3
            elif 100 > warning_score >= 75:
                print("WARNING LV 3")
                #Remote On
            
            
            #If Remote OFF
                #Set Motor Data by CCU
            
            
            #Else Remote ON
                #Get Motor Data from TCU
            
            
            #If There Is Nothing Blocking Front
                #Sending Motor and Submotor Value
            acpe.Racing_Wheel_Test.Print_Input()
                    
                    
            #Else Something Blocking Front
            if not pedal_error:
                acpe.Mode_Controller.Control_Car()
            
            
            print("ACPE ACTIVE")
            
    except:
        print("END")
        
    finally:
        acpe.RC_Car.Stop_MOTOR()
        GPIO.cleanup()
        print("CLEAN")

#====================Main(END)==================