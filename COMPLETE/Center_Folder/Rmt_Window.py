import threading
import tkinter as tk
from tkinter import messagebox

global monitor_driver_en, remote_drive_en
monitor_driver_en = False
remote_drive_en = False

# 운전자 위험 알람 UI 창
def Create_Warning_Lv2_Window():
    lv2_window = tk.Tk()
    lv2_window.title("WARNING_ALART")

    def On_Confirm_Click():
        Set_Monitoring_Driver_Activate()
        lv2_window.destroy()

    def On_Exit_Click():
        lv2_window.destroy()

    # 경고 메시지 출력
    warning_message = tk.Label(lv2_window, text="운전자가 현재 졸음 상태입니다! 확인 해야합니다!", font=("Arial", 14))
    warning_message.grid(row=0, column=0)

    # 버튼
    button = tk.Button(lv2_window, text="CONFIRM", command=On_Confirm_Click,  height = 2, width = 10)
    button.grid(row=1, column=0)
    button = tk.Button(lv2_window, text="Exit", command=On_Exit_Click,  height = 2, width = 10)
    button.grid(row=1, column=1)
    
    lv2_window.mainloop()
    
def Create_Warning_Lv3_Window():
    lv3_window = tk.Tk()
    lv3_window.title("REMOTE ALERT")

    def On_Confirm_Click():
        Set_Remote_Drive_Activate()
        lv3_window.destroy()

    def On_Exit_Click():
        lv3_window.destroy()

    # 경고 메시지 출력
    remote_message = tk.Label(lv3_window, text="원격 운전을 하시겠습니까??", font=("Arial", 14))
    remote_message.grid(row=0, column=0)

    # 버튼
    button = tk.Button(lv3_window, text="CONFIRM", command=On_Confirm_Click,  height = 2, width = 10)
    button.grid(row=1, column=0)
    button = tk.Button(lv3_window, text="Exit", command=On_Exit_Click,  height = 2, width = 10)
    button.grid(row=1, column=1)
    
    lv3_window.mainloop()
    

def Show_Window(level):
    if level == 'Lv2':
        thread_debug = threading.Thread(
            target=Create_Warning_Lv2_Window,
            args=()
        )
        thread_debug.start()
    if level == 'Lv3':
        thread_debug = threading.Thread(
            target=Create_Warning_Lv3_Window,
            args=()
        )
        thread_debug.start()
        

# Show_Window('Lv2')
# Show_Window('Lv3')

# 플래그 및 값 GET/SET 함수들
#region API Set

#region LV3

def Get_Monitoring_Driver_State():
    global monitor_driver_en
    return monitor_driver_en

def Set_Monitoring_Driver_Activate():
    global monitor_driver_en
    monitor_driver_en = True

def Set_Monitoring_Driver_Deactivate():
    global monitor_driver_en
    monitor_driver_en = False    

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

#endregion API Set
