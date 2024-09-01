import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Lv1_Warning as lv1

form_class = uic.loadUiType("C:\\SeonMin\\Embedded_SW\\Window\\ui\\Lv1\\Lv1_Warning.ui")[0] 

class Mywindow(QMainWindow, form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Button_Warning.clicked.connect(self.Btn_Warning_Clicked)
    
    def Btn_Warning_Clicked(self):
        print("Button Clicked!")
        QApplication.quit()
        

def Show_Window():
    app = QApplication(sys.argv)
    myWindow = Mywindow()
    myWindow.show()
    app.exec_()

if __name__ == "__main__":
    Show_Window()