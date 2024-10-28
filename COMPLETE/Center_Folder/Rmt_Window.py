import threading
import tkinter as tk
from tkinter import messagebox

global monitor_driver_en, remote_drive_en, remote_Forced_Activate, lv2_wind_en
monitor_driver_en = False
remote_drive_en = False
lv2_wind_en = False
remote_forced_activate = 0

# 운전자 위험 알람 UI 창
def Create_Warning_Lv2_Window():
    lv2_window = tk.Tk()
    lv2_window.title("WARNING_ALART")
    lv2_window.geometry('520x280+0+0')
    Set_LV2_Window_Activate()
    
    def On_Confirm_Click():
        Set_Monitoring_Driver_Activate()
        lv2_window.destroy()

    def On_Exit_Click():
        Set_LV2_Window_Deactivate()
        lv2_window.destroy()


    frame_1=tk.Frame(lv2_window, width=500, height=200, bg='#BFBFBF',bd=10,relief="ridge").place(x=10, y=10)
	
    # 경고 메시지 출력
    tk.Label(frame_1, text="[334부9870] 차량\n운전자 상태 이상 감지\n영상 확인 요청.",font=("Helvetica",34),bg='#BFBFBF').place(x=30, y=30)
    
    # 버튼
    button = tk.Button(lv2_window, text="CONFIRM", command=On_Confirm_Click, font=(34), height = 2, width = 20)
    button.place(x=20, y=215)
    button = tk.Button(lv2_window, text="Exit", command=On_Exit_Click, font=(34), height = 2, width = 20)
    button.place(x=260, y=215)
    
    lv2_window.mainloop()
    
def Create_Warning_Lv3_Window():
    lv3_window = tk.Tk()
    lv3_window.title("REMOTE ALERT")
    lv3_window.geometry('720x240+0+0')

    def On_Confirm_Click():
        Set_Remote_Drive_Activate()
        lv3_window.destroy()

    def On_Exit_Click():
        lv3_window.destroy()

    
    frame_1=tk.Frame(lv3_window, width=700, height=160, bg='#BFBFBF',bd=10,relief="ridge").place(x=10, y=10)
	
    # 메시지 출력
    tk.Label(frame_1, text="[334부9870] 차량\n원격 운전을 시행하시겠습니까?",font=("Helvetica",34),bg='#BFBFBF').place(x=30, y=30)
    
    # 버튼
    button = tk.Button(lv3_window, text="CONFIRM", command=On_Confirm_Click, font=(34), height = 2, width = 30)
    button.place(x=20, y=175)
    button = tk.Button(lv3_window, text="Exit", command=On_Exit_Click, font=(34), height = 2, width = 30)
    button.place(x=380, y=175)
    
    lv3_window.mainloop()
    
def Create_Remote_Active_Window():
    remote_Window = tk.Tk()
    remote_Window.title("Remote Activate UI")
    remote_Window.geometry('430x240+0+0')

    def On_Button_Active_Click():
        Set_Remote_Forced_Activate()

    def On_Button_Deactive_Click():
        Set_Remote_Forced_Deactivate()
    
    frame_1=tk.Frame(remote_Window, width=410, height=160, bg='#BFBFBF',bd=10,relief="ridge").place(x=10, y=10)
	
    # 메시지 출력
    tk.Label(frame_1, text="[334부9870] 차량\n 긴급 원격 운전",font=("Helvetica",34),bg='#BFBFBF').place(x=30, y=30)

    # 버튼
    button = tk.Button(remote_Window, text="ACTIVATE", command=On_Button_Active_Click, font=(34), height = 2, width = 16)
    button.place(x=20, y=175)
    button = tk.Button(remote_Window, text="DEACTIVATE", command=On_Button_Deactive_Click, font=(34), height = 2, width = 16)
    button.place(x=220, y=175)

    remote_Window.mainloop()

def Show_Window(level):
    if level == 'Lv2':
        thread_window = threading.Thread(
            target=Create_Warning_Lv2_Window,
            args=()
        )
        thread_window.start()
    if level == 'Lv3':
        thread_window = threading.Thread(
            target=Create_Warning_Lv3_Window,
            args=()
        )
        thread_window.start()
    if level == 'Remote_Select':
        thread_window = threading.Thread(
            target=Create_Remote_Active_Window,
            args=()
        )
        thread_window.start()
        

#Show_Window('Lv2')
# Show_Window('Lv3')
# Show_Window('Remote_Select')


# 플래그 및 값 GET/SET 함수들
#region API Set

#region LV2

def Get_Monitoring_Driver_State():
    global monitor_driver_en
    return monitor_driver_en

def Set_Monitoring_Driver_Activate():
    global monitor_driver_en
    monitor_driver_en = True

def Set_Monitoring_Driver_Deactivate():
    global monitor_driver_en
    monitor_driver_en = False    

def Get_LV2_Window_State():
    global lv2_wind_en
    return lv2_wind_en

def Set_LV2_Window_Activate():
    global lv2_wind_en
    lv2_wind_en = True

def Set_LV2_Window_Deactivate():
    global lv2_wind_en
    lv2_wind_en = False
    
#endregion LV2

#region LV3

def Get_Remote_Drive_State():
    global remote_drive_en
    return remote_drive_en

def Set_Remote_Drive_Activate():
    global remote_drive_en
    remote_drive_en = True

def Set_Remote_Drive_Deactivate():
    global remote_drive_en
    remote_drive_en = False    

#endregion LV2

#region Remote Forced

def Get_Remote_Forced_State():
    global remote_forced_activate
    return remote_forced_activate

def Set_Remote_Forced_Default():
    global remote_forced_activate
    remote_forced_activate = 0

def Set_Remote_Forced_Activate():
    global remote_forced_activate
    remote_forced_activate = 1

def Set_Remote_Forced_Deactivate():
    global remote_forced_activate
    remote_forced_activate = 2

#endregion Remote Forced

#endregion API Set
