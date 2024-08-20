import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("test.ui")[0]

class My_Window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        #QMessageBox.about(self, "message", "clicked")
        #여기에 원하는 이벤트 추가 가능
        #이 함수는 버튼이 눌리면 실행되는 함수라서, 소문자로 표시할 예정

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = My_Window()
    myWindow.show()
    app.exec_()