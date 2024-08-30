import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
import Racing_Wheel.RcVehicleCode_phk_240822.test_phk_240821_0958_Motor_Socket.TCU_Socket_Receive as TCU_Socket_Receive
from time import sleep  #time 라이브러리의 sleep함수 사용
import time
GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD

# sudo service uv4l_raspicam restart


#===============[Setup_Servo Motor]====================
GPIOPIN_Servo     = 16   # 서보 핀 (GPIO)
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기 
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기
GPIO.setup(GPIOPIN_Servo, GPIO.OUT)  # 서보핀 출력으로 설정
servo = GPIO.PWM(GPIOPIN_Servo, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.
Servo_Degree = 0 # 0 to 180


#===============[Setup_Go Motor]====================
MOTER_A_A1=20 # Go_Motor_A1 Pin Number (GPIO)
MOTER_A_B1=21 # Go_Motor_B1 Pin Number (GPIO)

GPIO.setup(MOTER_A_A1,GPIO.OUT)
GPIO.setup(MOTER_A_B1,GPIO.OUT)
MOTER_A_A1_PWM=GPIO.PWM(MOTER_A_A1,20)
MOTER_A_A1_PWM.start(0)
GPIO.output(MOTER_A_A1,GPIO.LOW)
GPIO.output(MOTER_A_B1,GPIO.LOW)
GoMotor_duty = 0  # 0 to 100







'''
서보 위치 제어 함수
degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
'''
def setServoPos(Servo_degree):
  # 각도는 180도를 넘을 수 없다.
  if Servo_degree > 180:
    Servo_degree = 180

  # 각도(degree)를 duty로 변경한다.
  servo_duty = SERVO_MIN_DUTY+(Servo_degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # duty 값 출력
  print("Degree: {} to {}(Duty)".format(Servo_degree, servo_duty))

  # 변경된 duty값을 서보 pwm에 적용
  servo.ChangeDutyCycle(servo_duty)


  



try :
    conn = TCU_Socket_Receive.start_server()
    while True :
        print("Running...")
        Handle_Degree, GoMotor_duty, Pedal_Brake = TCU_Socket_Receive.while_server(conn) # RacingWheel_Signal from Socket
        print("Handle   Degree: ",Handle_Degree)
        Servo_Degree = int((-Handle_Degree/2)+90)  #   -90 to 90  ==>  90 to -90  ==>  45 to 135
        print("Servo    Degree: ",Servo_Degree)
        print("DC Motor Power : ",GoMotor_duty)
        print("Pedal_Brake : ",Pedal_Brake)
        
        if Pedal_Brake != 0:  # if Press Brake: DCmotor = 0
            GoMotor_duty = 0
        
        MOTER_A_A1_PWM.ChangeDutyCycle(GoMotor_duty)
        setServoPos(Servo_Degree)

        
        print("")

        
finally :
    MOTER_A_A1_PWM.stop()

    GPIO.cleanup()

