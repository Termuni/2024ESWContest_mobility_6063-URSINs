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
            
#Pygame Test용 클래스입니다.
                    """
class Test_Pygame:
    '''
    파이게임 라이브러리 테스트용 클래스입니다.
    모니터 및 입력 테스트용으로, 실제 코드에는 적용하지 않을 예정이니 참고 부탁드립니다.
    
    Test_Pygame_Monitor_Set() -> 화면 생성을 위해 사용하는 함수, 테스트용으로 실 코드 적용 시 불필요
    -> 파이게임 통해 운전 가능한지 확인하기 위한 코드
    '''
    
    def __init__(self, screen = 0, my_square = 0, my_square_color = 0, colors = 0, motion = 0, forward = 1):
        self.screen, self.my_square, self.my_square_color, self.colors, self.motion = self.Test_Init_Pygame_Monitor_Set()
    
    #Test용 화면 생성용 함수
    def Test_Init_Pygame_Monitor_Set(self):
        pygame.display.set_caption('game base')
        self.screen = pygame.display.set_mode((1000, 1000), 0, 32)
        self.my_square = pygame.Rect(50, 50, 50, 50)
        self.my_square_color = 0
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.motion = [0, 0]
        return self.screen, self.my_square, self.my_square_color, self.colors, self.motion
    
    #Test용 화면 그리는 함수
    def Test_Pygame_Monitor_Draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.colors[self.my_square_color], self.my_square)
        if abs(self.motion[0]) < 0.1:
            self.motion[0] = 0
        if abs(self.motion[1]) < 0.1:
            self.motion[1] = 0
        self.my_square.x += self.motion[0] * 10
        self.my_square.y += self.motion[1] * 10
            
    #Wheel Input 받는 함수, 해당 부분 재 구현 예정
    def Test_Input_Wheel(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.my_square_color = (self.my_square_color + 1) % len(self.colors)
                elif event.button == 4:
                    self.forward = -1
                elif event.button == 5:
                    self.forward = 1
            #if event.type == pygame.JOYBUTTONUP:
                
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    self.motion[0] = event.value
                elif event.axis == 5:
                    self.motion[1] = (event.value + 1) / 2 * self.forward
                elif event.axis == 2:
                    self.motion[1] = 0
            #if event.type == pygame.JOYHATMOTION:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        """
'''
MAIN
'''

#변수 받은 뒤, while로 반복 시작
try:
    #Init
    Racing_Wheel_Test = Racing_Wheel()
    #Test_Monitor_N_Btn = Test_Pygame()

    #Loop
    while True:
        #Test_Monitor_N_Btn.Test_Pygame_Monitor_Draw()
        
        #Test_Monitor_N_Btn.Test_Input_Wheel()

        #pygame.display.update()
        
        Racing_Wheel_Test.Print_Input()
        
        Racing_Wheel_Test.clock.tick(60)

except:
    pygame.quit()
# except KeyboardInterrupt:
