import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  #time 라이브러리의 sleep함수 사용

GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD

class RC_Car_Control_Class:
    '''
    해당 클래스는 RC카를 제어하기 위한 클래스로
    클래스 호출 시 servo모터와 dc모터값을 설정합니다.
    MOTOR_A_A1의 PIN = 20 / MOTOR_A_B1의 PIN = 21 로 세팅되어 있으며
    servo, dc_pwm, dcMotor_Power, servo_Degree를 조정 가능
    '''
    
    #====================[INIT]========================
    def __init__(self, MOTOR_A_A1 = 20, MOTOR_A_B1 = 21, MOTOR_A_A1_PWM = 0, 
                 servo = 0, dc_pwm = 0, dcMotor_Power = 0, servo_Degree = 0):
        # DcMotor_Power = 0  # 0 to 100
        # Servo_Degree = 0 # 0 to 180
        self.Setup_Servo_Motor()
        self.Setup_DC_Motor()
        
    
    #===============[Setup_DC Motor]====================
    def Setup_DC_Motor(self, MOTOR_PWM_FREQUENCY = 20):
        '''
        이 함수는 기본적으로 PWM_Frequency, 모터 A_A1과 A_B1 의 값이 설정되어있습니다.
        PWM_Frequency = 20 / A_A1 = 20 / A_B1 = 21
        PWM_Frequency 값만 설정하려면 인자 하나만 입력하시면 됩니다.
        각 A_A1, A_B1 값은 GPIO 핀 값입니다.
        '''
        # MOTOR_A_A1          = 20 # DC모터 핀1 
        # MOTOR_A_B1          = 21 # DC모터 핀2 
        # MOTOR_PWM_FREQUENCY = 20 # PWM Frequency

        GPIO.setup(self.MOTOR_A_A1,GPIO.OUT)
        GPIO.setup(self.MOTOR_A_B1,GPIO.OUT)
        
        self.MOTOR_A_A1_PWM = GPIO.PWM(self.MOTOR_A_A1, MOTOR_PWM_FREQUENCY)
        self.MOTOR_A_A1_PWM.start(0)
        GPIO.output(self.MOTOR_A_A1,GPIO.LOW)
        GPIO.output(self.MOTOR_A_B1,GPIO.LOW)
    
    
    #===============[STOP_DC Motor]====================
    def Stop_MOTOR(self):
        self.MOTER_A_A1_PWM.stop()
        #MOTER_B_A1_PWM.stop()
        
        
    #===============[Setup_Servo Motor]====================
    def Setup_Servo_Motor(self, SERVO_PWM_HZ = 50, GPIOPIN_SERVO = 12):
        '''
        이 함수는 기본적으로 PWM_Hz, SERVO의 PIN값이 설정되어있습니다.
        PWM_Hz = 50 / GPIOPIN_SERVO = 12
        PWM_Hz 값만 설정하려면 인자 하나만 입력하시면 됩니다.
        '''
        # GPIOPIN_SERVO     = 12   # 서보모터 핀
        # SERVO_PWM_HZ      = 50   # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
        GPIO.setup(GPIOPIN_SERVO, GPIO.OUT)  # 서보핀 출력으로 설정
        self.servo = GPIO.PWM(GPIOPIN_SERVO, SERVO_PWM_HZ)  
        self.servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.


    #===============[Setup_Servo POS]====================
    def setServoPos(self, Servo_degree):
        '''
        서보 위치 제어 함수
        degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
        '''
        SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
        SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기
        # 각도는 180도를 넘을 수 없다.
        if Servo_degree > 180:
            Servo_degree = 180

        # 각도(degree)를 duty로 변경한다.
        servo_duty = SERVO_MIN_DUTY+(Servo_degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
        # duty 값 출력
        print("Degree: {} to {}(Duty)".format(Servo_degree, servo_duty))

        # 변경된 duty값을 서보 pwm에 적용
        self.servo.ChangeDutyCycle(servo_duty)









try :
    #Init 
    RC_Car = RC_Car_Control_Class()
    
    while True :
        #MOTER_A_A1_PWM.ChangeDutyCycle(DcMotor_Power)
        #setServoPos(Servo_Degree)
        print("DC Motor Power : ", RC_Car.dcMotor_Power)
        print("Servo    Degree: ",RC_Car.servo_Degree)
        print("")
        time.sleep(0.5)
        #print("Running...")
        
finally :
    RC_Car.Stop_MOTOR()
    GPIO.cleanup()
