'''
이 스크립트에서 각 레벨별 윈도우 부를 예정입니다.
'''
#import
import sys, os

window_path = "C:/SeonMin/Embedded_SW/Window/ui"
sub_paths = ["Lv1", "Lv2"]#, "Lv3", "Lv4"]

for sub_path in sub_paths:
    full_path = os.path.join(window_path, sub_path)
    
    # 경로를 sys.path에 추가
    if full_path not in sys.path:
        sys.path.append(full_path)

#==================CUSTOM IMPORT==================
import Lv1_Warning_Caller as lv1
import Lv2_Warning_Caller as lv2
#==================CUSTOM IMPORT==================

def Show_Window(level):
    if level == 1:
        lv1.Show_Window()
    if level == 2:
        lv2.Show_Window()
        