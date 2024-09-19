import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Lv1_Warning as lv1

#form_class = uic.loadUiType("C:\\SeonMin\\Embedded_SW\\COMPLETE\\CCU_Folder\\ui\\Lv1\\Lv1_Warning.ui")[0]
form_class = uic.loadUiType("/home/ursins/Desktop/2024ESWContest_mobility_6063-URSINs/COMPLETE/CCU_Folder/ui/Lv1/Lv1_Warning.ui")[0]

class Mywindow(QDialog, form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Button_Warning.clicked.connect(self.Btn_Warning_Clicked)
        self.flag_Clicked = False
    
    def Btn_Warning_Clicked(self):
        self.flag_Clicked = True
        
    def Close_Window(self):
        QApplication.quit()


def Show_Window():
    global myWindow
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()

# Show_Window()

#region API Set

def Get_BTN_Clicked():
    global myWindow
    return myWindow.flag_Clicked

def Close_LV1_Window():
    global myWindow
    myWindow.Close_Window()
    
#endregion API Set
