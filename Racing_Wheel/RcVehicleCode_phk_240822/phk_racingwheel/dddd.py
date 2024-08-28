import RPi.GPIO as GPIO
import time
#import Adafruit_DHT
#sensor=Adafruit_DHT.DHT11
MOTER_A_A1=5
MOTER_A_B1=6
MOTER_B_A1=20
MOTER_B_B1=21

GPIO.setmode(GPIO.BCM)

GPIO.setup(MOTER_A_A1,GPIO.OUT)
GPIO.setup(MOTER_A_B1,GPIO.OUT)
GPIO.setup(MOTER_B_A1,GPIO.OUT)
GPIO.setup(MOTER_B_B1,GPIO.OUT)

MOTER_A_A1_PWM=GPIO.PWM(MOTER_A_A1,20)
MOTER_B_A1_PWM=GPIO.PWM(MOTER_B_A1,20)
MOTER_A_A1_PWM.start(0)
MOTER_B_A1_PWM.start(0)

GPIO.output(MOTER_A_B1,GPIO.LOW)
GPIO.output(MOTER_B_B1,GPIO.LOW)

TMP_PIN=13
try :
    while True :
        #humidity, temperature = Adafruit_DHT.read_retry(sensor, TMP_PIN)
        #if humidity is not None and temperature is not None:
        #    print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        #else:
        #    print('Failed to get reading. Try again!')
        #duty=0;
        #if temperature > 25 and temperature < 28:
        #elif temperature > 27 and temperature < 30:
        #elif temperature > 29 and temperature < 32:
        #    duty=60
        #elif temperature > 31:
        #    duty=100
        #    duty=0
            duty=0
        MOTER_A_A1_PWM.ChangeDutyCycle(duty)
        MOTER_B_A1_PWM.ChangeDutyCycle(duty)
        time.sleep(0.5)
finally :
    MOTER_A_A1_PWM.stop()
    MOTER_B_A1_PWM.stop()
    GPIO.cleanup()