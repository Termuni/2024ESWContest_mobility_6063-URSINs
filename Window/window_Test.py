import WindowCall as wind
import time

wind.Show_Window('Debug')

while True:
    if wind.Get_Debug_Mode():
        if (wind.Get_Debug_Warning_Score() >= 50) and (not wind.Get_Lv1_Flag()):
            wind.Set_Debug_Lv1_Flag_Active()
            wind.Show_Window('Lv1')
    print(wind.Get_Debug_Warning_Score())
    time.sleep(0.3)