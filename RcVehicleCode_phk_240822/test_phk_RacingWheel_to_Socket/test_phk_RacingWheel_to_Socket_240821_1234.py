import sys
import pygame
from pygame.locals import *
import socket
import time
#http://192.168.0.8:8080/
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
        print("RacingWheel Input.. Searching...")
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #print(event.joy, event.axis, event.value)
                if event.axis == 0:        #Handle  -1 ~ 1
                    print("Moving Handle")
                    print(int(event.value *90))   # -90 ~ 90
                    return(0,int(event.value *90))
                
                elif event.axis == 2:      #Brake  0 ~ 100
                    print("Step Brake")
                    print(int(event.value *50 +50))
                    return(2,int(event.value *50 +50))
                
                elif event.axis == 5:      #Accel  0 ~ 100
                    print("Step ACCEL")
                    print(int(event.value *5 +5))
                    return(1,int(event.value *50 +50))
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
        # if. No Event  --> Brake = 0
        print("RacingWheel Input.. No Sig...(2,0)")
        return(2,0)
            


#변수 받은 뒤, while로 반복 시작
#try:
Racing_Wheel_Test = Racing_Wheel()
int_handle = 0
int_accel = 0
int_brake = 0

host = '192.168.0.5'
port = 9090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    Racing_Wheel_object,Racing_Wheel_value = Racing_Wheel_Test.Print_Input()
    #Racing_Wheel_Test.clock.tick(60)
    print("RacingWheel and Socket.. Running...")
    try:
        if Racing_Wheel_object == 0:   # Handle
            int_handle = Racing_Wheel_value
        elif Racing_Wheel_object == 1: # Accel
            int_accel = Racing_Wheel_value
        elif Racing_Wheel_object == 2: # Brake  
            int_brake = Racing_Wheel_value
        elif Racing_Wheel_object == 9: # No Signal...
            pass
        else:
            print("sig_Racing_Wheel Err!")
        result_str = str(int_handle) +'a'+ str(int_accel) +'a'+ str(int_brake)+'z'
    except Exception as e:
        print("Error...0a0a0z, because :",e)
        result_str = '0a0a0z'
    
    s.sendall(result_str.encode())
    print("Socket Signal Send Complete!\n")
    time.sleep(0.1)
        
        
#except:
#    pygame.quit()
#    print("END...")

# except KeyboardInterrupt:







