import time
import sys
import pygame
import threading
from pygame.locals import *


class Racing_Wheel:
    '''
    해당 코드는 파이게임(pygame) 이라는 라이브러리를 응용하여 조이스틱 값을 받고 사용합니다.
    함수는 다음과 같습니다.
    선언 시, 파이게임용 시간과 조이스틱을 반환합니다.
    
    Init_Racing_Wheel() -> 시작용 함수, 파이게임 시간을 반환, clock, joystick 반환
    '''
    def __init__(self, status = 0, verbose = False):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
        self.status = status
        self.verbose = verbose
        self.wheel_Value = [0, 0]
    
    #Racing Wheel 관련 시작 함수 실행, clock과 joystick을 반환함
    def Init_Racing_Wheel(self):
        pygame.init()
        pygame.joystick.init()
        self.clock = self.Set_Clock()
        self.joysticks = self.Get_Joystick()
        return self.clock, self.joysticks
    
    def Set_Clock(self):
        self.clock = pygame.time.Clock()
        return self.clock
    
    def Get_Joystick(self):
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            print(joystick.get_name())
            joystick.init()
        return self.joysticks
    
    def Update_Input_Value(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.status = 0
                    self.wheel_Value[0] = max(750, min(2250, ((50*(event.value* 10)) + 1500)))
                elif event.axis == 2:
                    self.status = 2
                    self.wheel_Value[1] = max(0, self.wheel_Value[1] - int(event.value *5 +5))
                elif event.axis == 5:
                    self.status = 5
                    self.wheel_Value[1] = min(100, self.wheel_Value[1] + int(event.value *5 +5))
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    print("Button_Bottom Input")
                elif event.button == 1:
                    print("Button_Right Input")
                elif event.button == 2:
                    print("Button_Left Input")
                elif event.button == 3:
                    print("Button_Up Input")
                else:
                    print("Button_else Input")
    
def Init_Wheel():
    global Racing_Wheel_Set
    #변수 초기화
    Racing_Wheel_Set = Racing_Wheel()

#region ============================ Threading Set (TOP) ============================

def Threading_RacingWheel():
    global Racing_Wheel_Set
    try:
        while True:
            Racing_Wheel_Set.Update_Input_Value()
    except KeyboardInterrupt:
        print("RacingWheel Check Stopped")


#endregion ============================ Threading Set (BOTTOM) ============================
    
#region ============================ API Set (TOP) ============================

# . Racing Wheel
def Get_Racing_Wheel_Status():
    global Racing_Wheel_Set
    return Racing_Wheel_Set.status

def Get_Racing_Wheel_Value():
    global Racing_Wheel_Set
    return Racing_Wheel_Set.wheel_Value
#endregion ============================ API Set (BOTTOM) ============================
    
    
def Init_Get_Wheel_Value():
    global Racing_Wheel_Set
    try:
        racing_wheel_thread = threading.Thread(
            target=Threading_RacingWheel,
            args=()
        )
        # 스레딩 시작
        racing_wheel_thread.start()
        
    except KeyboardInterrupt:
        print("monitoring stopped")
    
