import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
#from time import sleep  #time 라이브러리의 sleep함수 사용
import time
import sys
import pygame
from pygame.locals import *

GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD

global DcMotor_Power

class Racing_Wheel:
    '''
    해당 코드는 파이게임(pygame) 이라는 라이브러리를 응용하여 조이스틱 값을 받고 사용합니다.
    함수는 다음과 같습니다.
    선언 시, 파이게임용 시간과 조이스틱을 반환합니다.
    
    Init_Racing_Wheel() -> 시작용 함수, 파이게임 시간을 반환, clock, joystick 반환
    '''
    def __init__(self, clock = 0, joysticks = 0, status = 0, verbose = False):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
        self.status = status
        self.verbose = verbose
    
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
    
    def Get_Input(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:        #Handle  -10 ~ 0 ~ 10
                    return int(event.value * 10)
                    # print(int(event.value *10))
                    # new_servo_degree = RC_Car.servo_Degree + event.value * 10
                    # RC_Car.servo_Degree = max(20, min(160, new_servo_degree))
                elif event.axis == 2:      #Brake  0 ~ 10
                    return int(event.value *5 +5) 
                    # print(int(event.value *5 +5))
                    # new_power = RC_Car.dcMotor_Power - (event.value * 5 + 5)
                    # RC_Car.dcMotor_Power = max(0, new_power)
                elif event.axis == 5:      #Accel  0 ~ 10
                    return int(event.value *5 +5) 
                    # print(int(event.value *5 +5))
                    # new_power = RC_Car.dcMotor_Power + (event.value * 5 + 5)
                    # RC_Car.dcMotor_Power = min(100, new_power)
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
    
class RC_Car_Control:
    '''
    해당 클래스는 RC카를 제어하기 위한 클래스로
    클래스 호출 시 servo모터와 dc모터값을 설정합니다.
    MOTOR_A_A1의 PIN = 23 / MOTOR_A_B1의 PIN = 24 로 세팅되어 있으며
    servo, dc_pwm, dcMotor_Power, servo_Degree를 조정 가능
    '''
    #====================[INIT]========================
    def __init__(self, DcMotor_Power = 50, Servo_Degree = 90, GPIOPIN_MOTOR_A1 = 23, GPIOPIN_MOTOR_B1 = 24, GPIOPIN_MOTOR_A1_PWM= 0, 
                 servo = 0, dc_pwm = 0, dcMotor_Power = 0, servo_Degree = 0, verbose = False):
        self.GPIOPIN_MOTOR_A1 = GPIOPIN_MOTOR_A1
        self.GPIOPIN_MOTOR_B1 = GPIOPIN_MOTOR_B1
        self.GPIOPIN_MOTOR_A1_PWM = GPIOPIN_MOTOR_A1_PWM
        self.servo = servo
        self.dc_pwm = dc_pwm
        self.dcMotor_Power = DcMotor_Power
        self.servo_Degree = Servo_Degree
        self.Setup_Servo_Motor()
        self.Setup_DC_Motor()
        self.verbose = verbose
        
    #===============[Setup_DC Motor]====================
    def Setup_DC_Motor(self, MOTOR_PWM_FREQUENCY = 20):
        '''
        이 함수는 기본적으로 PWM_Frequency, 모터 A_A1과 A_B1 값 설정
        PWM_Frequency = 20 / A_A1 = 20 / A_B1 = 21
        PWM_Frequency 값만 설정하려면 인자 하나만 입력하시면 됩니다.
        각 A_A1, A_B1 값은 GPIO 핀 값입니다.
        '''
        MOTOR_PWM_FREQUENCY = 20 # PWM Frequency
        GPIO.setup(self.GPIOPIN_MOTOR_A1, GPIO.OUT)
        GPIO.setup(self.GPIOPIN_MOTOR_B1, GPIO.OUT)
        self.GPIOPIN_MOTOR_A1_PWM = GPIO.PWM(self.GPIOPIN_MOTOR_A1, MOTOR_PWM_FREQUENCY)
        self.GPIOPIN_MOTOR_A1_PWM.start(0)
        GPIO.output(self.GPIOPIN_MOTOR_A1, GPIO.LOW)
        GPIO.output(self.GPIOPIN_MOTOR_B1, GPIO.LOW)
    
    #===============[STOP_DC Motor]====================
    def Stop_MOTOR(self):
        self.GPIOPIN_MOTOR_A1_PWM.stop()
        
        if self.verbose == True:
            print("STOP MOTOR")
    
    #===============[Change_DUTY_DC Motor]====================
    def Change_Duty_Cycle(self):
        self.GPIOPIN_MOTOR_A1_PWM.ChangeDutyCycle(self.dcMotor_Power)
        print(f"dcMotor_Power = {self.dcMotor_Power}")
        
    #===============[Setup_Servo Motor]====================
    def Setup_Servo_Motor(self, SERVO_PWM_HZ = 50, GPIOPIN_SERVO = 17):
        '''
        이 함수는 기본적으로 PWM_Hz, SERVO의 PIN값이 설정되어있습니다.
        PWM_Hz = 50 / GPIOPIN_SERVO = 12
        PWM_Hz 값만 설정하려면 인자 하나만 입력하시면 됩니다.
        '''
        GPIOPIN_SERVO     = 17   # 서보모터 핀
        SERVO_PWM_HZ      = 50   # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
        GPIO.setup(GPIOPIN_SERVO, GPIO.OUT)  # 서보핀 출력으로 설정
        self.servo = GPIO.PWM(GPIOPIN_SERVO, SERVO_PWM_HZ)  
        self.servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.

    #===============[Setup_Servo POS]====================
    def Set_Servo_Pos(self, Servo_degree):
        '''
        서보 위치 제어 함수
        degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
        '''
        SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
        SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기
        
        # 조향각 범위 지정: 55 ~ 180
        if Servo_degree > 125:
            Servo_degree = 125
        if Servo_degree < 55:
            Servo_degree = 55

        # 각도(degree)를 duty로 변경한다.
        servo_duty = SERVO_MIN_DUTY+(Servo_degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
        
        # duty 값 출력
        if self.verbose == True:
            print("Degree: {} to {}(Duty)".format(Servo_degree, servo_duty))

        # 변경된 duty값을 서보 pwm에 적용
        self.servo.ChangeDutyCycle(servo_duty)
        print(f"servo_degree = {Servo_degree}")