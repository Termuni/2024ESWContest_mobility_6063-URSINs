import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Debug

form_class = uic.loadUiType("C:\\SeonMin\\Embedded_SW\\COMPLETE\\CCU_Folder\\ui\\Debug\\Debug.ui")[0] 
flag_Clicked = False

class Mywindow(QDialog, form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #region DATA
        self.d_ppg_lv = 0
        self.d_ecg_lv = 0
        self.d_cam_lv = 0
        self.d_pedal_err = False
        self.debug_mode = False
        #endregion DATA
        
        #region BTN CONNECT
        self.Debug_Mode_Change.clicked.connect(self.DEBUG_MODE_CHANGE)
        self.bpm_set.clicked.connect(self.BPM_SET)
        self.cam_set.clicked.connect(self.CAM_SET)
        self.Pedal_ERR_Set.clicked.connect(self.UDAS_SET)
        self.ALL_SET.clicked.connect(self.EVERYTHING_SET)
        #endregion BTN CONNECT
        
    def DEBUG_MODE_CHANGE(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.Debug_Mode_Text.setText("Debug_Mode_Available")
        else:
            self.Debug_Mode_Text.setText("Debug_Mode_Disabled")
    
    def BPM_SET(self):
        if (self.ppg_lv_text.text() != '') and (self.ppg_lv_text.text() != ''):
            self.d_ppg_lv = int(self.ppg_lv_text.text())
            self.d_ecg_lv = int(self.ecg_lv_text.text())
        print(f"BPM SET (ppg, ecg) : {self.d_ppg_lv, self.d_ecg_lv}")
    
    def CAM_SET(self):
        if (self.cam_lv_text.text() != ''):
            self.d_cam_lv = int(self.cam_lv_text.text())
        print(f"CAM SET : {self.d_cam_lv}")
    
    def UDAS_SET(self):
        self.d_pedal_err = self.Pedal_ERR.isChecked()
        print(f"Pedal ERR : {self.d_pedal_err}")
        
    def EVERYTHING_SET(self):
        if (self.ppg_lv_text.text() != '') and (self.ppg_lv_text.text() != '') and (self.cam_lv_text.text() != ''):
            self.d_ppg_lv = int(self.ppg_lv_text.text())
            self.d_ecg_lv = int(self.ecg_lv_text.text())
            self.d_cam_lv = int(self.cam_lv_text.text())
            self.d_pedal_err = self.Pedal_ERR.isChecked()
        print(f"EVERYTHING SET\nppg_lv={self.d_ppg_lv}, ecg_lv={self.d_ecg_lv}, cam_lv={self.d_cam_lv}, pedal_err={self.d_pedal_err}")

    def Close_Window(self):
        QApplication.quit()


def Show_Window():
    global flag_Clicked, myWindow
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()
    #return app

#region API Set

def Get_Debug_PPG_LV():
    global myWindow
    return myWindow.d_ppg_lv

def Get_Debug_ECG_LV():
    global myWindow
    return myWindow.d_ecg_lv

def Get_Debug_CAM_LV():
    global myWindow
    return myWindow.d_cam_lv

def Get_Debug_Pedal_ERR():
    global myWindow
    return myWindow.d_pedal_err

def Get_Debug_Mode():
    global myWindow
    return myWindow.debug_mode

def Close_Debug_Window():
    global myWindow
    myWindow.Close_Window()

#endregion API Set

# Show_Window()