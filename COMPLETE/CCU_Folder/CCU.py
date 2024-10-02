#import
import sys, os
import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import time
import os


#region File Path Control
# file_path = "C:/SeonMin/Embedded_SW"
# sub_paths = ["ACPE", "Communication", "HeartBeat", "Window"]

# for sub_path in sub_paths:
#     full_path = os.path.join(file_path, sub_path)
    
#     # 경로를 sys.path에 추가
#     if full_path not in sys.path:
#         sys.path.append(full_path)
#endregion File Path Control

#==================CUSTOM IMPORT==================
import UDAS as udas
import BPM as bpm
import WindowCall as wind
import Warning_Score_Calculator as warn
import UART_Communication as wcom
import MP3 as mp3
#==================CUSTOM IMPORT==================

#Set Constant Values

def Init_CCU():
    global GPIO
    global pedal_error
    global ppg_lv, ecg_lv
    global cTt_Ser, dTc_Ser, tcp, data_to_TCU, data_to_DMU, data_from_DMU, data_from_TCU
    global cam_lv, warning_score
    global debug_mode, mode_change_input, has_lv1_Warned, has_lv2_Warned, has_lv3_Warned, has_remote_Warned, remote_Mode, wheel_Value, time_counter
    
    GPIO.cleanup()
    
    # 1. SET GPIO
    GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
    #GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD
    print("1:COMPLETED")
    
    # 2. Init acpe
    pedal_error = False
    udas.Init_UDAS()
    udas.Init_Get_UltraSonic_Distance()
    print("2:COMPLETED")
    
    # 3. Init bpm
    ppg_lv = 0
    ecg_lv = 0
    # bpm.Init_BPM()
    # bpm.Init_Get_BPM_Data()
    print("3:COMPLETED")
    
    # 4. Init Monitor
    wind.Show_Window('Watch')
    time.sleep(0.3)
    wind.Show_Window('Debug')
    print("4:COMPLETED")
    
    # 5. Init Communication
    cTt_Ser = wcom.Init_UART(port="/dev/serial0") #CCU ~ TCU Serial
    dTc_Ser = wcom.Init_UART(port="/dev/ttyAMA3") #CCU ~ DMU Serial
    data_to_TCU = "Hello TCU\n"
    data_from_TCU = '0'
    data_from_DMU = '0'
    data_to_DMU = 'test\n'
    print("5:COMPLETED")
    
    # 6. SET extra Datas
    debug_mode = False
    mode_change_input = False
    has_lv1_Warned = False
    has_lv2_Warned = False
    has_lv3_Warned = False
    has_remote_Warned = False
    remote_Mode = False
    wheel_Value = [0, 0]
    cam_lv = 0
    warning_score = 0
    time_counter = 0
    print("6:COMPLETED")
    
    

def Debug_INPUT():
    global ppg_lv, ecg_lv, cam_lv, pedal_error, warning_score
    ppg_lv, ecg_lv, cam_lv, pedal_error, warning_score = wind.Get_Debug_All()


#====================Main(START)==================

if __name__ == "__main__":

    try:
        #INIT VALUES
        Init_CCU()
        print("START PROCESSING")
        
        while True:
            print("========================================")
            # ================ . Debug Mode Set ================
            debug_mode = wind.Get_Debug_Mode()
            
            # ================ . Get Datas And Calculate By Algorithm================
            #If Debug Mode
            if debug_mode:
                Debug_INPUT()
            #Else Getting Sensor Value
            else:
                data_from_DMU = wcom.Receive_Data(dTc_Ser) #Data from DMU (only Receive)
                data_from_TCU = wcom.Receive_Data(cTt_Ser)
                dmu_datas = data_from_DMU.split(',')
                tcu_datas = data_from_TCU.split(',')
                if len(dmu_datas) < 3:
                    ppg_lv = 0
                    ecg_lv = 0
                    cam_lv = 0
                elif ((dmu_datas[0].isdecimal()) and (dmu_datas[1].isdecimal())) and (dmu_datas[2].isdecimal()):
                    ppg_lv = int(dmu_datas[0])
                    ecg_lv = int(dmu_datas[1])
                    cam_lv = int(dmu_datas[2])
                pedal_error = udas.Check_Pedal_Error()
                
            #Calculate By Datas AND Update Data
            warning_score = warn.Calculate_Warning_Score(
                    ppg_lv, ecg_lv, cam_lv, pedal_error, warning_score)
            
            wind.Set_Watch_Values(ppg_lv, ecg_lv, cam_lv, pedal_error, warning_score)
            
            udas.Update_Racing_Wheel()
            
    #region ==================== . Warning LV (In Progress)====================
            if warning_score < 0:
                warning_score = 0
                
            #If Warning LV 0                 
            elif 25 >= warning_score >= 0:
                data_to_TCU = '0'
                
            #Elif Warning LV 1
            elif 50 > warning_score >= 25:
                data_to_TCU = '1'
                if not has_lv1_Warned:    
                    #LCD Alarm
                    has_lv1_Warned = True
                    mp3.Play_MP3("LV1.mp3")
                    wind.Show_Window('Lv1')
                    wind.Set_Debug_Lv1_Flag_Active()
                else:
                    if (has_lv1_Warned) and (wind.Get_Lv1_Flag()):
                        warning_score = warning_score + 0.01
                    else:
                        has_lv1_Warned = False
                        warning_score = 0
            
            #Elif Warning LV 2  (Sound, LED Needed)
            elif 75 > warning_score >= 50:
                data_to_TCU = '2'
                print("WARNING LV 2")
                if not has_lv2_Warned:
                    #Sound Output
                    has_lv2_Warned = True
                    mp3.Play_MP3("LV2.mp3")
                #LED ON
            
            #Elif Warning LV 3                  
            elif 100 >= warning_score >= 75:
                data_to_TCU = '3'
                print("WARNING LV 3")
                if not has_remote_Warned:
                    has_remote_Warned = True
                    mp3.Play_MP3("Remote_Mode.mp3")
                #Sound Output
                #External ALARM
                
            elif warning_score > 100:
                warning_score = 100
                
            # ---------------- .2 Send And Receive Warning Lv ----------------
            #Send Warning LV to TCU
            wcom.Send_Data(cTt_Ser, data_to_TCU)  # 데이터 전송
            
            #Check Remote Mode
            if len(tcu_datas) < 3:
                remote_Mode = False
            elif (int(tcu_datas[0]) == 4):
                remote_Mode = True
            
            # ---------------- .3 Set Remote Mode ----------------
            #If Remote OFF
            if not remote_Mode:
                print("Manual Drive")
                #Set Motor Data by CCU
                wheel_Value = udas.Get_Racing_Wheel_Value()
            
            #Else Remote ON
            else:
                print("Remote Drive")
                #Get Motor Data from TCU
                wheel_Value[0] = int(tcu_datas[1])
                wheel_Value[1] = int(tcu_datas[2])
            
            #endregion Warning LV
            
            # ================ . ACPE ================
            #If There Is Nothing Blocking Front
            if pedal_error:
                udas.Set_RC_Car_DcMotor_Power(0)
                udas.Update_RC_Car_Duty_Cycle()
                time.sleep(2)
            
            if not pedal_error:
                #Sending Motor and Submotor Value
                udas.Set_RC_Car_Servo_Pos(wheel_Value[0])
                udas.Set_RC_Car_DcMotor_Power(wheel_Value[1])
                udas.Update_RC_Car_Duty_Cycle()

            # ================ . Timer ================
            if(time_counter == 50):
                time_counter = 0
                has_lv2_Warned = False
                has_remote_Warned = False
                
            time_counter = time_counter + 1
   
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("END")
        GPIO.cleanup()
        
        
    finally:
        wcom.Close_UART(cTt_Ser)
        wcom.Close_UART(dTc_Ser)
        udas.RC_Car_Set.Stop_MOTOR()
        #GPIO.cleanup()
        print("CLEAN")

#====================Main(END)==================
