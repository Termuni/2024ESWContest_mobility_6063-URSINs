import RPi.GPIO as GPIO 
import time
import sys
import pygame
from pygame.locals import *

GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD

class Communication_Remote_Center:
    '''
    원격 센터로부터의 제어 정보(패킷)을 수신하고 해석하기 위한 클래스
    manual 제어 모드에서도 통신은 유지되어야 하며 데이터 패킷 구성은 다음과 같다.(mode, 조향각, 페달)
    '''
    #====================[INIT]========================
    def __init__(self, GPIOPIN_COM = 26, verbose = False, steering_command_from_center = 110, power_command_from_center = 40):
        self.verbose = verbose
        self.GPIOPIN_COM = GPIOPIN_COM
        self.steering_command_from_center = steering_command_from_center
        self.power_command_from_center = power_command_from_center 
        GPIO.setup(self.GPIOPIN_COM, GPIO.IN)

    #===============[패킷 데이터 해석]==================
    def Interpret_Packet(self):
        # packet = GPIO.input(self.GPIOPIN_COM)
        packet = [0, 111, 41]
        
        if packet[0] == 0:
            Mode_Controller.mode = 'manual'
        elif packet[0] == 1:
            Mode_Controller.mode = 'remote'
    
        self.steering_command_from_center = packet[1]    
        self.power_command_from_center = packet[2]
    
        if self.verbose == True:
            print("패킷 데이터 확인")
            print(f"패킷 정보: mode={Mode_Controller.mode}, steering_angle={self.steering_command_from_center}, pedal={self.power_command_from_center}")


class Mode_Control:
    '''
    원격 센터로부터 수신한 데이터 패킷(제어 모드 정보)에 따라 차량을 제어하기 위한 클래스
    - manual(직접 제어) 모드
    - remote(원격 센터 제어) 모드 
    '''
    #====================[INIT]========================
    def __init__(self, mode = 'manual', verbose = False):
        self.mode = mode
        self.verbose = False
    
    ''' 
    사용 X
    def Switch_Mode(self, new_mode):
        if new_mode in ['manual', 'remote']:
            self.mode = new_mode
            print(f"차량 제어권 변경: {self.mode}")
        else:
            print("유효하지 않은 모드입니다. 기존 모드를 유지합니다.")
    '''

    #=============[모터 / 서보모터 제어]================
    def Control_Car(self):
        if self.mode == 'manual':
            RC_Car.Change_Duty_Cycle()
            RC_Car.setServoPos()

        elif self.mode == 'remote':
            RC_Car.dcMotor_Power = Communication_With_Remote_Center.power_command_from_center
            RC_Car.servo_Degree = Communication_With_Remote_Center.steering_command_from_center
            RC_Car.Change_Duty_Cycle()
            RC_Car.setServoPos()            
        if self.verbose == True:
            print(f"현재 제어 모드: {self.mode}")


class RC_Car_Control:
    '''
    RC카 제어를 위해 모터와 서보모터를 셋업 및 제어하는 클래스
    '''
    
    #====================[INIT]========================
    def __init__(self, GPIOPIN_MOTOR_A1 = 23, GPIOPIN_MOTOR_B1 = 24, GPIOPIN_MOTOR_A1_PWM= 0, 
                 servo = 0, dcMotor_Power = 50, servo_Degree = 90, verbose = False):
        self.GPIOPIN_MOTOR_A1 = GPIOPIN_MOTOR_A1
        self.GPIOPIN_MOTOR_B1 = GPIOPIN_MOTOR_B1
        self.GPIOPIN_MOTOR_A1_PWM = GPIOPIN_MOTOR_A1_PWM
        self.servo = servo
        self.dcMotor_Power = dcMotor_Power
        self.servo_Degree = servo_Degree
        self.Setup_Servo_Motor()
        self.Setup_DC_Motor()
        self.verbose = verbose
        
    #=========[모터 PIN / PWM 주파수 세팅]==============
    def Setup_DC_Motor(self, MOTOR_PWM_FREQUENCY = 20):
        GPIOPIN_MOTOR_A1          = 23 
        GPIOPIN_MOTOR_B1          = 24 
        MOTOR_PWM_FREQUENCY       = 20 

        GPIO.setup(self.GPIOPIN_MOTOR_A1, GPIO.OUT)
        GPIO.setup(self.GPIOPIN_MOTOR_B1, GPIO.OUT)
        
        self.GPIOPIN_MOTOR_A1_PWM = GPIO.PWM(self.GPIOPIN_MOTOR_A1, MOTOR_PWM_FREQUENCY)
        self.GPIOPIN_MOTOR_A1_PWM.start(0)
        GPIO.output(self.GPIOPIN_MOTOR_A1, GPIO.LOW)
        GPIO.output(self.GPIOPIN_MOTOR_B1, GPIO.LOW)
    
    #================[모터 속도 제어]==================
    def Change_Duty_Cycle(self):
        self.GPIOPIN_MOTOR_A1_PWM.ChangeDutyCycle(self.dcMotor_Power)
        print(f"dcMotor_Power = {self.dcMotor_Power}")
        
    #==========[서보 모터 PIN / 주파수 세팅]===========
    def Setup_Servo_Motor(self, SERVO_PWM_HZ = 50, GPIOPIN_SERVO = 17):
        GPIOPIN_SERVO     = 17   
        SERVO_PWM_HZ      = 50   # 50Hz > 20ms
        GPIO.setup(GPIOPIN_SERVO, GPIO.OUT)  
        self.servo = GPIO.PWM(GPIOPIN_SERVO, SERVO_PWM_HZ)  
        self.servo.start(0)

    #=========[서보 모터 duty 계산 및 적용]============
    def setServoPos(self):

        SERVO_MAX_DUTY    = 12  
        SERVO_MIN_DUTY    = 3  
        
        # 각도(degree)를 duty로 변경
        servo_duty = SERVO_MIN_DUTY+(self.servo_Degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)

        self.servo.ChangeDutyCycle(servo_duty)
        print(f"servo_degree = {self.servo_Degree}")
        if self.verbose == True:
            print("Degree: {} to {}(Duty)".format(self.servo_Degree, servo_duty))

class Racing_Wheel:
    '''
    POWER SHIFT 스티어링 휠 / 페달을 통해 RC카를 제어하기 위한 클래스
    작품 구동을 위한 핸들, 브레이크, 액셀 기능만 적용
    '''

    #====================[INIT]========================
    def __init__(self, clock = 0, joysticks = 0, status = 0, verbose = False):   
        self.clock, self.joysticks = self.Init_Racing_Wheel()
        self.status = status
        self.verbose = verbose
    
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
    
    #=============[스티어링 휠 / 페달 EVENT 기반 RC카 제어]============
    def Print_Input(self):
        self.status = -1
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:        #Handle: -10 ~ 0 ~ 10
                    self.status = 0
                    print(int(event.value *10))
                    new_servo_degree = RC_Car.servo_Degree + event.value * 10
                    RC_Car.servo_Degree = max(20, min(160, new_servo_degree))
                    if self.verbose == True:
                        print("Moving Handle")
                    
                elif event.axis == 2:      #Brake: 0 ~ 10
                    self.status = 2
                    print(int(event.value *5 +5))
                    new_power = RC_Car.dcMotor_Power - (event.value * 5 + 5)
                    RC_Car.dcMotor_Power = max(0, new_power)
                    if self.verbose == True:
                        print("Step Brake")
                    
                elif event.axis == 5:      #Accel: 0 ~ 10
                    self.status = 5
                    print(int(event.value *5 +5))
                    new_power = RC_Car.dcMotor_Power + (event.value * 5 + 5)
                    RC_Car.dcMotor_Power = min(100, new_power)
                    if self.verbose == True:
                        print("Step ACCEL")
                        
                    
class ADAS:
    '''
    초음파 센서를 이용해 장애물과의 거리를 측정하고 운전자의 페달 오조작을 방지하는 클래스
    - ACPE: Anti-Pedal Misapplication Error
    - AEB: Autonomous Emergency Braking system
    '''
    #====================[INIT]========================
    def __init__(self, GPIOPIN_TRIG = 5, GPIOPIN_ECHO = 6, DANGER_DISTANCE = 40, verbose = False):
        self.GPIOPIN_TRIG = GPIOPIN_TRIG
        self.GPIOPIN_ECHO = GPIOPIN_ECHO
        self.DANGER_DISTANCE = DANGER_DISTANCE
        self.verbose = verbose
        self.Initiate_ADAS()

    #================[초음파 센서 셋업]=================
    def Initiate_ADAS(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIOPIN_TRIG, GPIO.OUT)
        GPIO.setup(self.GPIOPIN_ECHO, GPIO.IN)
        GPIO.output(self.GPIOPIN_TRIG, False)

    #=============[장애물과의 거리 계산]================
    def Measure_Distance(self):
        GPIO.output(self.GPIOPIN_TRIG, True)
        time.sleep(0.01)
        GPIO.output(self.GPIOPIN_TRIG, False)

        pulse_start = time.time()
        while GPIO.input(self.GPIOPIN_ECHO) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(self.GPIOPIN_ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150

        if distance <= -500 or distance >= 500:
            return None

        return distance

    def Get_Stable_Distance(self, samples = 5):
        distances = []
        for _ in range(samples):
            distance = self.Measure_Distance()
            if distance is not None:
                distances.append(distance)

        if len(distances) > 0:
            if self.verbose == True:
                print(f"stable distance = {sum(distances) / len(distances)}")
            return sum(distances) / len(distances)
        else:
            print("ultrasonic sensor do not working !!")
            return None           

    #============[페달 오조작 여부 판단]===============
    def Check_Pedal_Error(self):
        distance = self.Get_Stable_Distance()
        if distance is None:
            return False

#        if distance < self.DANGER_DISTANCE and Racing_Wheel_Test.status == 5:
        if distance < self.DANGER_DISTANCE:
            print("페달 오조작 감지. 가속 제한.")
            RC_Car.setServoPos()

            if RC_Car.dcMotor_Power > 1:
                RC_Car.dcMotor_Power = 1
                return True
        else:
            if self.verbose == True:
                print("정상적인 조작 감지중")
            return False
                    

# Init 
RC_Car = RC_Car_Control()
Racing_Wheel_Test = Racing_Wheel()
ADAS_System = ADAS()
Communication_With_Remote_Center = Communication_Remote_Center()
Mode_Controller = Mode_Control()

print("Init Complete")

try:
    while True :
        Communication_With_Remote_Center.Interpret_Packet()
        pedal_error = ADAS_System.Check_Pedal_Error()

        if not pedal_error:
            Mode_Controller.Control_Car()
            
        Racing_Wheel_Test.Print_Input()
        time.sleep(0.05)
        
        print("===========================")
        print("")
        
finally :
    RC_Car.Stop_MOTOR()
    GPIO.cleanup()
