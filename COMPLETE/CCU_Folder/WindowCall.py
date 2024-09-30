import threading
import tkinter as tk
from tkinter import messagebox

global lv1_activate, debug_mode_en, d_ppg_lv, d_ecg_lv, d_cam_lv, d_pedal_err, d_warning_score
global w_ppg_lv, w_ecg_lv, w_cam_lv, w_pedal_err, w_warning_score
lv1_activate = False
debug_mode_en = False
d_ppg_lv = 0  # PPG_LV 디폴트 값
d_ecg_lv = 0  # ECG_LV 디폴트 값
d_cam_lv = 0  # CAM_LV 디폴트 값
d_warning_score = 0  # Warning Score 디폴트 값

# 디버그 UI 창
def Create_Debug_Window():
    global debug_mode_en, d_ppg_lv, d_ecg_lv, d_cam_lv, d_pedal_err, d_warning_score
    debug_Window = tk.Tk()
    debug_Window.title("Debug UI")
    
    # Debug 모드 변수
    debug_mode = tk.StringVar(value="Debug_Mode_Disabled")
    debug_mode_en = False

    def Toggle_Debug_Mode():
        global debug_mode_en
        debug_mode_en = not debug_mode_en
        if debug_mode.get() == "Debug_Mode_Disabled":
            debug_mode.set("Debug_Mode_Enabled")
        else:
            debug_mode.set("Debug_Mode_Disabled")
    
    # PPG_LV, ECG_LV, CAM_LV의 초기값 설정
    ppg_lv_var = tk.StringVar(value=str(d_ppg_lv))
    ecg_lv_var = tk.StringVar(value=str(d_ecg_lv))
    cam_lv_var = tk.StringVar(value=str(d_cam_lv))
    warning_score_var = tk.StringVar(value=str(d_warning_score))

    # BPM (PPG_LV, ECG_LV)
    tk.Label(debug_Window, text="BPM").grid(row=0, column=0)
    tk.Label(debug_Window, text="PPG_LV").grid(row=1, column=0)
    ppg_lv = tk.Entry(debug_Window, textvariable=ppg_lv_var)
    ppg_lv.grid(row=1, column=1)
    tk.Button(debug_Window, text="SET", command=lambda: [Set_Debug_PPG_Lv(ppg_lv.get()), print(f"PPG_LV SET: {ppg_lv.get()}")]).grid(row=1, column=2)

    tk.Label(debug_Window, text="ECG_LV").grid(row=2, column=0)
    ecg_lv = tk.Entry(debug_Window, textvariable=ecg_lv_var)
    ecg_lv.grid(row=2, column=1)
    tk.Button(debug_Window, text="SET", command=lambda: [Set_Debug_ECG_Lv(ecg_lv.get()), print(f"ECG_LV SET: {ecg_lv.get()}")]).grid(row=2, column=2)

    # Debug 모드 전환 버튼
    tk.Label(debug_Window, textvariable=debug_mode).grid(row=0, column=3)
    tk.Button(debug_Window, text="DEBUG_MODE_CHANGE", command=Toggle_Debug_Mode).grid(row=1, column=3)

    # CAM (CAM_LV)
    tk.Label(debug_Window, text="CAM").grid(row=3, column=0)
    tk.Label(debug_Window, text="CAM_LV").grid(row=4, column=0)
    cam_lv = tk.Entry(debug_Window, textvariable=cam_lv_var)
    cam_lv.grid(row=4, column=1)
    tk.Button(debug_Window, text="SET", command=lambda: [Set_Debug_CAM_Lv(cam_lv.get()), print(f"CAM_LV SET: {cam_lv.get()}")]).grid(row=4, column=2)

    # UDAS (Pedal Err 체크박스)
    tk.Label(debug_Window, text="UDAS").grid(row=5, column=0)
    pedal_err = tk.IntVar()
    tk.Checkbutton(debug_Window, text="Pedal Err", variable=pedal_err).grid(row=6, column=0)
    tk.Button(debug_Window, text="SET", command=lambda: [Set_Debug_Pedal_Err(pedal_err.get()), print(f"Pedal Err SET: {pedal_err.get()}")]).grid(row=6, column=2)

    # Warning Score 설정
    tk.Label(debug_Window, text="Warning Score").grid(row=7, column=0)
    warning_score = tk.Entry(debug_Window, textvariable=warning_score_var)
    warning_score.grid(row=7, column=1)
    tk.Button(debug_Window, text="SET", command=lambda: [Set_Debug_Warning_Score(warning_score.get()), print(f"Warning Score SET: {warning_score.get()}")]).grid(row=7, column=2)

    # ALL SET 버튼
    tk.Button(debug_Window, text="ALL SET", command=lambda: Set_Debug_ALL(ppg_lv.get(), ecg_lv.get(), cam_lv.get(), pedal_err.get(), warning_score.get())).grid(row=8, column=2, rowspan=6)

    debug_Window.mainloop()

def Create_Watch_Window():
    global w_ppg_lv, w_ecg_lv, w_cam_lv, w_pedal_err, w_warning_score
    
    w_ppg_lv = 0
    w_ecg_lv = 0
    w_cam_lv = 0
    w_pedal_err = False
    w_warning_score = 0
    
    watch_Window = tk.Tk()
    watch_Window.title("Watcher UI")
    
    # PPG_LV, ECG_LV, CAM_LV의 값 확인
    ppg_lv_var = tk.StringVar(value=str(w_ppg_lv))
    ecg_lv_var = tk.StringVar(value=str(w_ecg_lv))
    cam_lv_var = tk.StringVar(value=str(w_cam_lv))
    pedal_err_var = tk.StringVar(value=str(w_pedal_err))
    warning_score_var = tk.StringVar(value=str(w_warning_score))

    # BPM (PPG_LV, ECG_LV)
    tk.Label(watch_Window, text="BPM").grid(row=0, column=0)
    tk.Label(watch_Window, text="PPG_LV").grid(row=1, column=0)
    ppg_lv = tk.Entry(watch_Window, textvariable=ppg_lv_var)
    ppg_lv.grid(row=1, column=1)
    tk.Label(watch_Window, text="ECG_LV").grid(row=2, column=0)
    ecg_lv = tk.Entry(watch_Window, textvariable=ecg_lv_var)
    ecg_lv.grid(row=2, column=1)
    
    # CAM (CAM_LV)
    tk.Label(watch_Window, text="CAM").grid(row=3, column=0)
    tk.Label(watch_Window, text="CAM_LV").grid(row=4, column=0)
    cam_lv = tk.Entry(watch_Window, textvariable=cam_lv_var)
    cam_lv.grid(row=4, column=1)
    
    # UDAS (Pedal Err 체크박스)
    tk.Label(watch_Window, text="Pedal ERR").grid(row=5, column=0)
    pedal_err = tk.Entry(watch_Window, textvariable=pedal_err_var)
    pedal_err.grid(row=4, column=1)

    # Warning Score 설정
    tk.Label(watch_Window, text="Warning Score").grid(row=7, column=0)
    warning_score = tk.Entry(watch_Window, textvariable=warning_score_var)
    warning_score.grid(row=7, column=1)
    
    watch_Window.mainloop()

# 위험Lv1 UI 창
def Create_Warning_Lv1_Window():
    window2 = tk.Tk()
    window2.title("WANING UI")

    def On_Button_Click():
        Set_Debug_Lv1_Flag_Deactive()
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
            target=Create_Debug_Window,
            args=()
        )
        thread_debug.start()
    elif level == 'Watch':
        thread_watch = threading.Thread(
            target=Create_Watch_Window,
            args=()
        )
        thread_watch.start()
    elif level == 'Lv1':
        Set_Debug_Lv1_Flag_Active()
        thread_lv1 = threading.Thread(
            target=Create_Warning_Lv1_Window,
            args=()
        )
        thread_lv1.start()
        

# Show_Window('Watch')

# 플래그 및 값 GET/SET 함수들
#region API Set

#region LV1

def Get_Lv1_Flag():
    global lv1_activate
    return lv1_activate

def Set_Debug_Lv1_Flag_Active():
    global lv1_activate
    lv1_activate = True

def Set_Debug_Lv1_Flag_Deactive():
    global lv1_activate
    lv1_activate = False

#endregion LV1

#region DEBUG

#region GET_DEBUG
def Get_Debug_Mode():
    global debug_mode_en
    return debug_mode_en

def Get_Debug_PPG_Lv():
    global d_ppg_lv
    if d_ppg_lv.isdecimal():
        return int(d_ppg_lv)

def Get_Debug_ECG_Lv():
    global d_ecg_lv
    if d_ecg_lv.isdecimal():
        return int(d_ecg_lv)

def Get_Debug_CAM_Lv():
    global d_cam_lv
    if d_cam_lv.isdecimal():
        return int(d_cam_lv)

def Get_Debug_Pedal_Err():
    global d_pedal_err
    if d_pedal_err.isdecimal():
        return int(d_pedal_err)

def Get_Debug_Warning_Score():
    global d_warning_score
    if d_warning_score.isdecimal():
        return int(d_warning_score)

def Get_Debug_All():
    return Get_Debug_PPG_Lv(), Get_Debug_ECG_Lv(), Get_Debug_CAM_Lv(), Get_Debug_Pedal_Err(), Get_Debug_Warning_Score()

#endregion GET_DEBUG

#region SET_DEBUG

def Set_Debug_PPG_Lv(level):
    global d_ppg_lv
    d_ppg_lv = level
    
def Set_Debug_ECG_Lv(level):
    global d_ecg_lv
    d_ecg_lv = level
    
def Set_Debug_CAM_Lv(level):
    global d_cam_lv
    d_cam_lv = level

def Set_Debug_Pedal_Err(err_value):
    global d_pedal_err
    d_pedal_err = err_value

def Set_Debug_Warning_Score(score):
    global d_warning_score
    d_warning_score = score
    
def Set_Debug_ALL(ppg_lv, ecg_lv, cam_lv, pedal_err, warning_score):
    Set_Debug_PPG_Lv(ppg_lv)
    Set_Debug_ECG_Lv(ecg_lv)
    Set_Debug_CAM_Lv(cam_lv)
    Set_Debug_Pedal_Err(pedal_err)
    Set_Debug_Warning_Score(warning_score)

#endregion Debug

#endregion DEBUG

#region WATCH

def Set_Watch_Values(ppg_lv, ecg_lv, cam_lv, pedal_err, warning_score):
    global w_ppg_lv, w_ecg_lv, w_cam_lv, w_pedal_err, w_warning_score
    w_ppg_lv = ppg_lv
    w_ecg_lv = ecg_lv
    w_cam_lv = cam_lv
    w_pedal_err = pedal_err
    w_warning_score = warning_score

#endregion WATCH

#endregion API Set



