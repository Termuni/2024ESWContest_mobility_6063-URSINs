# ��ȯ�̰� ���̽��� Ȱ���϶�� �Ѱ��� Base �ڵ���.
# �� �ڵ�� �������� �ʾƵ� �˴ϴ�. 

import sys
import pygame
from pygame.locals import *
import time

#Racing Wheel ���� Ŭ�����Դϴ�.
class Racing_Wheel:
    '''
    �ش� �ڵ�� ���̰���(pygame) �̶�� ���̺귯���� �����Ͽ� ���̽�ƽ ���� �ް� ����մϴ�.
    �Լ��� ������ �����ϴ�.
    ���� ��, ���̰��ӿ� �ð��� ���̽�ƽ�� ��ȯ�մϴ�.
    
    Init_Racing_Wheel() -> ���ۿ� �Լ�, ���̰��� �ð��� ��ȯ, clock, joystick ��ȯ
    '''

    def __init__(self, clock = 0, joysticks = 0):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
    
    #Racing Wheel ���� ���� �Լ� ����, clock�� joystick�� ��ȯ��
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
                if event.axis == 0:        #Handle  -10 ~ 0 ~ 10
                    print("Moving Handle")
                    print(int(event.value *10))
                elif event.axis == 2:      #Brake  0 ~ 10
                    print("Step Brake")
                    print(int(event.value *5 +5))
                elif event.axis == 5:      #Accel  0 ~ 10
                    print("Step ACCEL")
                    print(int(event.value *5 +5))
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
            

#���� ���� ��, while�� �ݺ� ����
try:
    Racing_Wheel_Test = Racing_Wheel()
    
    while True:
        Racing_Wheel_Test.Print_Input()
        time.sleep(0.1)

except:
    pygame.quit()
# except KeyboardInterrupt:

