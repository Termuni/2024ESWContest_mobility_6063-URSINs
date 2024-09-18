import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Debug

form_class = uic.loadUiType("C:\\SeonMin\\Embedded_SW\\Window\\ui\\Debug\\Debug.ui")[0] 
flag_Clicked = False

class Mywindow(QMainWindow, form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #region BTN CONNECT
        self.Debug_Mode_Change.clicked.connect(self.DEBUG_MODE_CHANGE)
        self.bpm_set.clicked.connect(self.BPM_SET)
        self.cam_set.clicked.connect(self.CAM_SET)
        self.Pedal_ERR_Set.clicked.connect(self.UDAS_SET)
        self.ALL_SET.clicked.connect(self.ALL_SET)
        #endregion BTN CONNECT
        
    def DEBUG_MODE_CHANGE(self):
        return 0
    
    def BPM_SET(self):
        return 1
    
    def CAM_SET(self):
        return 2
    
    def UDAS_SET(self):
        return 3
        
    def ALL_SET(self):
        return 4

def Show_Window():
    global flag_Clicked
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()
    return app

#Show_Window()