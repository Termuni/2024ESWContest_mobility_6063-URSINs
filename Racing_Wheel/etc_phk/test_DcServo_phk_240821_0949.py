import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  #time 라이브러리의 sleep함수 사용
GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD


# CCU에서, DC모터와 서보모터를 제어하기 위한 Base 코드.
# 지환이에게 넘겨준 코드임. 
# 최종 결과물에 사용하지 않을 코드.



#===============[Setup_Servo Motor]====================
GPIOPIN_Servo     = 12   # 서보모터 핀
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기
GPIO.setup(GPIOPIN_Servo, GPIO.OUT)  # 서보핀 출력으로 설정
servo = GPIO.PWM(GPIOPIN_Servo, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.



#===============[Setup_DC Motor]====================
MOTER_A_A1=20 # DC모터 핀1 
MOTER_A_B1=21 # DC모터 핀2 

GPIO.setup(MOTER_A_A1,GPIO.OUT)
GPIO.setup(MOTER_A_B1,GPIO.OUT)
MOTER_A_A1_PWM=GPIO.PWM(MOTER_A_A1,20)
MOTER_A_A1_PWM.start(0)
GPIO.output(MOTER_A_B1,GPIO.LOW)
GPIO.output(MOTER_B_B1,GPIO.LOW)



DcMotor_Power = 0  # 0 to 100
Servo_Degree = 0 # 0 to 180



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
    while True :
        #MOTER_A_A1_PWM.ChangeDutyCycle(DcMotor_Power)
        #setServoPos(Servo_Degree)
        print("DC Motor Power : ",DcMotor_Power)
        print("Servo    Degree: ",Servo_Degree)
        print("")
        time.sleep(0.5)
        #print("Running...")
finally :
    MOTER_A_A1_PWM.stop()
    MOTER_B_A1_PWM.stop()
    GPIO.cleanup()

