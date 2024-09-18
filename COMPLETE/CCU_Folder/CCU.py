#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time

# file_path = "C:/SeonMin/Embedded_SW"
# sub_paths = ["ACPE", "Communication", "HeartBeat", "Window"]

# for sub_path in sub_paths:
#     full_path = os.path.join(file_path, sub_path)
    
#     # 경로를 sys.path에 추가
#     if full_path not in sys.path:
#         sys.path.append(full_path)

#==================CUSTOM IMPORT==================
import ACPE_Renewal as acpe
import BPM as bpm
import WindowCall as wind
import Warning_Score_Calculator as warn
import TCP_IP_Communication as wlcom
import UART_Communication as wcom
#==================CUSTOM IMPORT==================

#Set Constant Values

def Init_CCU():
    global GPIO
    global pedal_error
    global serial, tcp
    global debug_mode, mode_change_input, warning_score, hasWarned, remote_Mode
    
    # 1. SET GPIO
    GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
    
    # 2. Init acpe
    acpe.Init_ACPE()
    acpe.Init_Get_UltraSonic_Distance()
    pedal_error = False
    
    # 3. Init bpm
    bpm.Init_BPM()
    bpm.Init_Get_BPM_Data()
    
    # 4. Init Monitor
    
    # 5. Init Communication
    serial = wcom.Init_UART()
    tcp = wlcom.Init_Client_Socket()
    
    # 6. SET extra Datas
    debug_mode = False
    mode_change_input = False
    warning_score = 0
    hasWarned = False
    remote_Mode = False
    


def Debug_INPUT(d_ppg_lv, d_ecg_lv, d_cam_lv, d_pedal_error, warning_score):
    #Debug Input Mode Activate
    warning_score = warn.Calculate_Warning_Score(d_ppg_lv, d_ecg_lv, d_cam_lv, d_pedal_error, warning_score)


#====================Main(START)==================

if __name__ == "__main__":

    try:
        #INIT VALUES
        Init_CCU()
        print("START PROCESSING")
        
        while True:
            # ================ 1. Debug Mode Set ================
            if mode_change_input:
                debug_mode = not debug_mode
                mode_change_input = not mode_change_input
                if debug_mode:
                    print("DEBUG MODE ACTIVATE")
                else:
                    print("DEBUG MODE DEACTIVATE")
                
                
            # ================ 2. Set Values of Racing Wheel ================
            acpe.Update_RC_Car_Duty_Cycle()
            
            
            # ================ 3. Warning Lv Calculate By Algorithm ================
            #If Debug Mode
            if debug_mode:
                # Debug_INPUT()
                0
                
            #Else Getting Sensor Value
            else:
                pedal_error = acpe.Check_Pedal_Error()
                cam_lv = 0
                warning_score = warn.Calculate_Warning_Score(bpm.ppg_bpm_level, bpm.ecg_bpm_level, cam_lv, pedal_error, warning_score)
                
            
            # ================ 4. Warning Lv Usage ================
            # ---------------- 4.1 Scoring Algorithm ----------------
            
            #                  If Warning LV 0                 
            if 25 >= warning_score >= 0:
                remote_Mode = False
                
            #                  If Warning LV 1                  
            elif 50 > warning_score >= 25:
                remote_Mode = False
                print("WARNING LV 1")
                if not hasWarned:    
                    #LCD Alarm
                    hasWarned = True
                    wind.Show_Window(1)
                else:
                    if (hasWarned) and (not wind.lv1.flag_Clicked):
                        #얼마나 빨리 많이 올릴 것인지?
                        warning_score = warning_score + 0.01
                    else:
                        warning_score = 0
            
            
            #                  Elif Warning LV 2                  
            elif 75 > warning_score >= 50:
                remote_Mode = False
                print("WARNING LV 2")
                #Sound Output
                #LED ON
            
            
            #                  Elif Warning LV 3                  
            elif 100 > warning_score >= 75:
                remote_Mode = True
                print("WARNING LV 3")
                #LCD Remote Control Alarm
                #External ALARM
                #Remote On
            
            # ---------------- 4.2 Send And Receive Warning Lv ----------------
            #Send Warning LV to TCU
            
            #Receive Score Setup From TCU -> Score Setup 0 or over 100 which set by Center
            
            
            # ---------------- 4.3 Set Remote Mode ----------------
            #If Remote OFF
            if not remote_Mode:
                print("Manual Drive")
                #Set Motor Data by CCU
            
            
            #Else Remote ON
            else:
                print("Remote Drive")
                #Get Motor Data from TCU
            
            
            # ================ 5. ACPE ================
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