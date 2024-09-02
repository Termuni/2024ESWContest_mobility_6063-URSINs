import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Lv1_Warning as lv1

form_class = uic.loadUiType("C:\\SeonMin\\Embedded_SW\\Window\\ui\\Lv1\\Lv1_Warning.ui")[0] 
flag_Clicked = False

class Mywindow(QMainWindow, form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Button_Warning.clicked.connect(self.Btn_Warning_Clicked)
    
    def Btn_Warning_Clicked(self):
        global flag_Clicked
        #print("Button Clicked!")
        flag_Clicked = True
        QApplication.quit()
        

def Show_Window():
    global flag_Clicked
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()
