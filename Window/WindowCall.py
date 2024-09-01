'''
이 스크립트에서 각 레벨별 윈도우 부를 예정입니다.
'''
#import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#==================CUSTOM IMPORT==================
from ui import Lv1_Warning_Caller as lv1
from ui import Lv2_Warning_Caller as lv2
#==================CUSTOM IMPORT==================

def Show_Window(level):
    if level == 1:
        lv1.Show_Warning_Message()
    if level == 2:
        lv2.Show_Warning_Message()
        
if __name__ == "__main__":
    level = input("레벨 입력 : ")
    Show_Window(level)