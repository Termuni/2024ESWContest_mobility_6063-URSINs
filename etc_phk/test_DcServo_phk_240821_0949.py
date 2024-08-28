import RPi.GPIO as GPIO #RPi.GPIO ���̺귯���� GPIO�� ���
from time import sleep  #time ���̺귯���� sleep�Լ� ���
GPIO.setmode(GPIO.BCM) #Pin Mode : GPIO
#GPIO.setmode(GPIO.BOARD)  #Pin Mode : BOARD


# CCU����, DC���Ϳ� �������͸� �����ϱ� ���� Base �ڵ�.
# ��ȯ�̿��� �Ѱ��� �ڵ���. 
# ���� ������� ������� ���� �ڵ�.



#===============[Setup_Servo Motor]====================
GPIOPIN_Servo     = 12   # �������� ��
SERVO_MAX_DUTY    = 12   # ������ �ִ�(180��) ��ġ�� �ֱ�
SERVO_MIN_DUTY    = 3    # ������ �ּ�(0��) ��ġ�� �ֱ�
GPIO.setup(GPIOPIN_Servo, GPIO.OUT)  # ������ ������� ����
servo = GPIO.PWM(GPIOPIN_Servo, 50)  # �������� PWM ��� 50Hz�� ����ϱ� (50Hz > 20ms)
servo.start(0)  # ���� PWM ���� duty = 0, duty�� 0�̸� ������ �������� �ʴ´�.



#===============[Setup_DC Motor]====================
MOTER_A_A1=20 # DC���� ��1 
MOTER_A_B1=21 # DC���� ��2 

GPIO.setup(MOTER_A_A1,GPIO.OUT)
GPIO.setup(MOTER_A_B1,GPIO.OUT)
MOTER_A_A1_PWM=GPIO.PWM(MOTER_A_A1,20)
MOTER_A_A1_PWM.start(0)
GPIO.output(MOTER_A_B1,GPIO.LOW)
GPIO.output(MOTER_B_B1,GPIO.LOW)



DcMotor_Power = 0  # 0 to 100
Servo_Degree = 0 # 0 to 180



'''
���� ��ġ ���� �Լ�
degree�� ������ �Է��ϸ� duty�� ��ȯ�� ���� ����(ChangeDutyCycle)
'''
def setServoPos(Servo_degree):
  # ������ 180���� ���� �� ����.
  if Servo_degree > 180:
    Servo_degree = 180

  # ����(degree)�� duty�� �����Ѵ�.
  servo_duty = SERVO_MIN_DUTY+(Servo_degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # duty �� ���
  print("Degree: {} to {}(Duty)".format(Servo_degree, servo_duty))

  # ����� duty���� ���� pwm�� ����
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

