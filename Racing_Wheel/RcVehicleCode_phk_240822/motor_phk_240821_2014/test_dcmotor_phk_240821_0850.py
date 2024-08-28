import RPi.GPIO as GPIO
import time

MOTER_A_A1=20
MOTER_A_B1=21
#MOTER_B_A1=2
#MOTER_B_B1=23

GPIO.setmode(GPIO.BCM)

GPIO.setup(MOTER_A_A1,GPIO.OUT)
GPIO.setup(MOTER_A_B1,GPIO.OUT)
#GPIO.setup(MOTER_B_A1,GPIO.OUT)
#GPIO.setup(MOTER_B_B1,GPIO.OUT)

MOTER_A_A1_PWM=GPIO.PWM(MOTER_A_A1,20)
#MOTER_B_A1_PWM=GPIO.PWM(MOTER_B_A1,20)
MOTER_A_A1_PWM.start(0)
#MOTER_B_A1_PWM.start(0)

GPIO.output(MOTER_A_B1,GPIO.LOW)
#GPIO.output(MOTER_B_B1,GPIO.LOW)
duty = 50

try :
    while True :
        MOTER_A_A1_PWM.ChangeDutyCycle(duty)
        #MOTER_B_A1_PWM.ChangeDutyCycle(duty)
        time.sleep(0.5)
        print("Running...")
finally :
    MOTER_A_A1_PWM.stop()
    #MOTER_B_A1_PWM.stop()
    GPIO.cleanup()