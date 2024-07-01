import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo pins declaration
SERVO_PINS = [7,11,13]
for servo in servo_pin:
    GPIO.setup(servo_pin[servo], GPIO.OUT)
servo1 = GPIO.PWM(servo_pin[0], 50)
servo2 = GPIO.PWM(servo_pin[1], 50)
servo3 = GPIO.PWM(servo_pin[2], 50)
servo1.start(0)
servo2.start(0)
servo3.start(0)
#Motor pins declaration
LEFT_MOTORS_PINS = [1,2,3,4]
RIGHT_MOTORS_PINS = [5,6,8,9]
for pin in LEFT_MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
for pin in RIGHT_MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)

class Move:
    def __init__(self):
        self.Servo()
    def Servo(self):
        servo1.ChangeDutyCycle(2 + (servo1_angle / 18))      
        servo2.ChangeDutyCycle(2 + (servo2_angle / 18))  
        servo3.ChangeDutyCycle(2 + (servo3_angle / 18))
    def motor(self):
        GPIO.output(stepper_motor_1_pins[pin], halfstep_seq[halfstep][pin])
        
               
            





