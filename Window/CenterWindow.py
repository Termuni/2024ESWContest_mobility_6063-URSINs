import threading
import tkinter as tk
from tkinter import messagebox


global remote_Forced_Activate
remote_forced_activate = False

def Create_Remote_Active_Window():
    remote_Window = tk.Tk()
    remote_Window.title("Remote Activate UI")

    def On_Button_Active_Click():
        Set_Remote_Forced_Activate()
        remote_Window.destroy()

    def On_Button_Cancel_Click():
        remote_Window.destroy()
        
    # 경고 메시지 출력
    warning_message = tk.Label(remote_Window, text="긴급 원격 운전", font=("Arial", 14))
    warning_message.grid(row=0, column=0)

    # 버튼
    button = tk.Button(remote_Window, text="ACTIVATE", command=On_Button_Active_Click)
    button.grid(row=1, column=0)
    button = tk.Button(remote_Window, text="EXIT", command=On_Button_Cancel_Click)
    button.grid(row=1, column=1)

    remote_Window.mainloop()

def Show_Window(level):
    if level == 'Remote_Activate':
        thread_remote_activate = threading.Thread(
            target=Create_Remote_Active_Window,
            args=()
        )
        thread_remote_activate.start()



#region API SET
def Get_Remote_Forced():
    global remote_forced_activate
    return remote_forced_activate

def Set_Remote_Forced_Activate():
    global remote_forced_activate
    remote_forced_activate = True

def Set_Remote_Forced_Deactivate():
    global remote_forced_activate
    remote_forced_activate = False
#endregion API SET