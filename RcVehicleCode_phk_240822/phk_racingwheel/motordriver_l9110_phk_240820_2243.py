import utime
import machine

motor1a = machine.Pin(10, machine.Pin.OUT)
motor1b = machine.Pin(11, machine.Pin.OUT)

led = machine.Pin(15, machine.Pin.OUT)
led.value(0)
utime.sleep(0.5)
led.value(1)
utime.sleep(0.5)
led.value(0)

#functions
def forward():
    led.value(1)
    motor1a.high()
    motor1b.low()
    
def backward():
    led.value(1)
    motor1a.low()
    motor1b.high()
    
def stop():
    led.value(0)
    motor1a.low()
    motor1b.low()
    
def testMotor():
    forward()
    utime.sleep(2)
    stop()
    utime.sleep(1)
    backward()
    utime.sleep(2)
    stop()
    utime.sleep(2)

print("OK...")
print("RPi-PICO with DC Motor")

while True:
        
    testMotor()