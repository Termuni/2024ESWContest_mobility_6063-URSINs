import sys
import pygame
from pygame.locals import *

#Racing Wheel 관련 클래스입니다.
class Racing_Wheel:
    '''
    해당 코드는 파이게임(pygame) 이라는 라이브러리를 응용하여 조이스틱 값을 받고 사용합니다.
    함수는 다음과 같습니다.
    선언 시, 파이게임용 시간과 조이스틱을 반환합니다.
    
    Init_Racing_Wheel() -> 시작용 함수, 파이게임 시간을 반환, clock, joystick 반환
    '''

    def __init__(self, clock = 0, joysticks = 0):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
    
    #Racing Wheel 관련 시작 함수 실행, clock과 joystick을 반환함
    def Init_Racing_Wheel(self):
        pygame.init()
        pygame.joystick.init()
        self.clock = self.Clock_Set()
        self.joysticks = self.Get_Joystick()
        return self.clock, self.joysticks
    
    def Clock_Set(self):
        self.clock = pygame.time.Clock()
        return self.clock
    
    def Get_Joystick(self):
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            print(joystick.get_name())
            joystick.init()
        return self.joysticks
    
    def Print_Input(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #print(event.joy, event.axis, event.value)
                if event.axis == 0:        #Handle
                    print("Moving Handle")
                    print(event.value *10)
                elif event.axis == 2:      #Brake
                    print("Step Brake")
                    print(event.value *5 +5)
                elif event.axis == 5:      #Accel
                    print("Step ACCEL")
                    print(event.value *5 +5)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    print("Button_Bottom Input")
                elif event.button == 1:
                    print("Button_Right Input")
                elif event.button == 2:
                    print("Button_Left Input")
                elif event.button == 3:
                    print("Button_Up Input")
                else :
                    print("Button_else Input")
                    print(event.button)
            

#변수 받은 뒤, while로 반복 시작
try:
    Racing_Wheel_Test = Racing_Wheel()
    
    while True:
        Racing_Wheel_Test.Print_Input()
        Racing_Wheel_Test.clock.tick(60)

except:
    pygame.quit()
# except KeyboardInterrupt:

