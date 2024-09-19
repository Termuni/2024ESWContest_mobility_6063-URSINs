import threading
import tkinter as tk
from tkinter import messagebox

global lv1_activate
lv1_activate = False

# 첫 번째 UI 창
def Create_Debug_Window():
    window1 = tk.Tk()
    window1.title("Debug UI")
    
    # Debug 모드 변수
    debug_mode = tk.StringVar(value="Debug_Mode_Disabled")

    def Toggle_Debug_Mode():
        if debug_mode.get() == "Debug_Mode_Disabled":
            debug_mode.set("Debug_Mode_Enabled")
        else:
            debug_mode.set("Debug_Mode_Disabled")
    
    # BPM (PPG_LV, ECG_LV)
    tk.Label(window1, text="BPM").grid(row=0, column=0)
    tk.Label(window1, text="PPG_LV").grid(row=1, column=0)
    ppg_lv = tk.Entry(window1)
    ppg_lv.grid(row=1, column=1)
    tk.Button(window1, text="SET", command=lambda: print("PPG_LV:", ppg_lv.get())).grid(row=1, column=2)

    tk.Label(window1, text="ECG_LV").grid(row=2, column=0)
    ecg_lv = tk.Entry(window1)
    ecg_lv.grid(row=2, column=1)
    tk.Button(window1, text="SET", command=lambda: print("ECG_LV:", ecg_lv.get())).grid(row=2, column=2)

    # Debug 모드 전환 버튼
    tk.Label(window1, textvariable=debug_mode).grid(row=0, column=3)
    tk.Button(window1, text="DEBUG_MODE_CHANGE", command=Toggle_Debug_Mode).grid(row=1, column=3)

    # CAM (CAM_LV)
    tk.Label(window1, text="CAM").grid(row=3, column=0)
    tk.Label(window1, text="CAM_LV").grid(row=4, column=0)
    cam_lv = tk.Entry(window1)
    cam_lv.grid(row=4, column=1)
    tk.Button(window1, text="SET", command=lambda: print("CAM_LV:", cam_lv.get())).grid(row=4, column=2)

    # UDAS (Pedal Err 체크박스)
    tk.Label(window1, text="UDAS").grid(row=5, column=0)
    pedal_err = tk.IntVar()
    tk.Checkbutton(window1, text="Pedal Err", variable=pedal_err).grid(row=6, column=0)
    tk.Button(window1, text="SET", command=lambda: print("Pedal Err:", pedal_err.get())).grid(row=6, column=2)

    # ALL SET 메시지
    tk.Button(window1, text="ALL SET", command=lambda: print(f"All Set: {ppg_lv.get(), ecg_lv.get(), cam_lv.get(), pedal_err.get()}")).grid(row=5, column=2, rowspan=6)

    window1.mainloop()

# 두 번째 UI 창
def Create_Warning_Lv1_Window():
    window2 = tk.Tk()
    window2.title("Second UI")

    def On_Button_Click():
        Set_Lv1_Flag_Deactive()
        window2.destroy()

    # 경고 메시지 출력
    warning_message = tk.Label(window2, text="조심하세요!! 지금 졸고 계십니다!!!", font=("Arial", 14))
    warning_message.grid(row=0, column=1)

    # 버튼
    button = tk.Button(window2, text="PushButton", command=On_Button_Click)
    button.grid(row=0, column=0)

    window2.mainloop()


def Show_Window(level):
    if level == 'Debug':
        thread_debug = threading.Thread(
            target= Create_Debug_Window,
            args=()
        )
        thread_debug.start()
    elif level == 'Lv1':
        Set_Lv1_Flag_Active()
        thread_lv1 = threading.Thread(
            target= Create_Warning_Lv1_Window,
            args=()
        )
        thread_lv1.start()
        
        
def Get_Lv1_Flag():
    global lv1_activate
    return lv1_activate

def Set_Lv1_Flag_Active():
    global lv1_activate
    lv1_activate = True
    
def Set_Lv1_Flag_Deactive():
    global lv1_activate
    lv1_activate = False