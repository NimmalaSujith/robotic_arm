import RPi.GPIO as GPIO
import time
from RpiMotorLib import RpiMotorLib
import speech_recognition as sr
import datetime

count =2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
recognizer = sr.Recognizer()

direction= 14 # Direction (DIR) GPIO Pin
step = 15 # Step GPIO Pin

GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
step_change = 0
change_1 = 0
change_2 = 0
present_servo1_position = 0
present_stepper_motor_main_position = 0
present_servo2_position = 0
present_servo3_position = 0
present_stepper_motor1_position = 0
present_stepper_motor2_position = 0

# Arm and motor pins numbers declaration
stepper_motor_1_pins = [ 19, 26, 21, 20]
stepper_motor_2_pins = [ 16, 12, 25, 24]
for x_pins in stepper_motor_1_pins:
    GPIO.setup(x_pins, GPIO.OUT)
    GPIO.output(x_pins,GPIO.LOW)
for x_pins in stepper_motor_2_pins:
    GPIO.setup(x_pins, GPIO.OUT)
#servo motor
servo_pin = [6,5,0]
GPIO.setup(servo_pin[0], GPIO.OUT)
GPIO.setup(servo_pin[1], GPIO.OUT)
GPIO.setup(servo_pin[2], GPIO.OUT)
servo1 = GPIO.PWM(servo_pin[0], 50)
servo2 = GPIO.PWM(servo_pin[1], 50)
servo3 = GPIO.PWM(servo_pin[2], 50)
servo1.start(0)
servo2.start(0)
servo3.start(0)
task = [(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20),(90,90,0,0,30,20)]
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def arm_move(main_motor,servo1_angle, servo2_angle, Stepper_motor1_angle, Stepper_motor2_angle,servo3_angle
                 ):
    # Arm present position global declaration
    global present_servo1_position
    global present_stepper_motor_main_position
    global present_servo2_position
    global present_servo3_position
    global present_stepper_motor1_position
    global present_stepper_motor2_position
    # Arm and motor pins global declaration
    global servo_pin
    global stepper_motor_1_pins
    global stepper_motor_2_pins
    global stepper_motor_main_pins
    
    global halfstep_seq
    global hello_seq
    global step_change
    global change_1
    global change_2
    while True:
        change_stepper_motor1 = round(1.4222222222 * Stepper_motor1_angle)
        change_stepper_motor2 = round(1.4222222222 * Stepper_motor2_angle)
        change_stepper_motor_main = main_motor
        servo1.ChangeDutyCycle(2 + (servo1_angle / 18))
        servo2.ChangeDutyCycle(2 + (servo2_angle / 18))
        servo3.ChangeDutyCycle(2 + (servo3_angle / 18))
        if present_stepper_motor_main_position != change_stepper_motor_main:
            if change_stepper_motor_main > present_stepper_motor_main_position:
                step_change = change_stepper_motor_main - present_stepper_motor_main_position
                is_true = True
                present_stepper_motor_main_position += step_change
            else :
                is_true = False
                step_change =present_stepper_motor_main_position -  change_stepper_motor_main
                present_stepper_motor_main_position -= step_change
            mymotortest.motor_go(is_true, # True=Clockwise, False=Counter-Clockwise
                         "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         step_change, # number of steps
                         .003, # step delay [sec]
                         False, # True = print verbose output 
                         .05) # initial delay [sec]
            print(step_change,is_true)
        if present_stepper_motor1_position != change_stepper_motor1:
            if change_stepper_motor1 > present_stepper_motor1_position:
                change_1 = change_stepper_motor1 - present_stepper_motor1_position
                for i in range(change_1):
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(stepper_motor_1_pins[pin], halfstep_seq[halfstep][pin])
                        time.sleep(0.002)
                present_stepper_motor1_position += change_1
            
            else :
                change_1 = present_stepper_motor1_position - change_stepper_motor1 
                for i in range(change_1):
                    for halfstep in range(7,-1,-1):
                        for pin in range(4):
                            GPIO.output(stepper_motor_1_pins[pin], halfstep_seq[halfstep][pin])
                        time.sleep(0.002)
                present_stepper_motor1_position -= change_1
            print(present_stepper_motor1_position)
        if present_stepper_motor2_position != change_stepper_motor2:
            if change_stepper_motor2 > present_stepper_motor2_position:
                change_2 = change_stepper_motor2 - present_stepper_motor2_position
                for i in range(change_2):
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(stepper_motor_2_pins[pin], halfstep_seq[halfstep][pin])
                        time.sleep(0.001)
                present_stepper_motor2_position += change_2
            else :
                change_2 = present_stepper_motor2_position - change_stepper_motor2 
                for i in range(change_2):
                    for halfstep in range(7,-1,-1):
                        for pin in range(4):
                            GPIO.output(stepper_motor_2_pins[pin], halfstep_seq[halfstep][pin])
                        time.sleep(0.001)
                present_stepper_motor2_position -= change_2
        
        
        if present_stepper_motor1_position == change_stepper_motor1 and present_stepper_motor2_position == change_stepper_motor2 :
            print("completed")
            break
def say_move(file_name,speed):
    with open(file_name + ".txt") as arm_file:
        for x_file in arm_file:
            task = x_file.readline().split(",")
            arm_move(int(task[0]),int(task[1]),int(task[2]),int(task[3]),int(task[4]),int(task[5]),speed)

        
while True:
    
    if count == 1:
        with sr.Microphone() as source:
            print('Clearing background noise...Please wait')
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("waiting for your message...")
            recordedaudio = recognizer.listen(source)
            print('Done recording')
            print(recordedaudio)
            #   print('Printing your message...Please wait')
            #   text = recognizer.recognize_google(recordedaudio, language='en-US')
            #   print('Your Message:{}', format(text))
            try:
                text = recognizer.recognize_google(recordedaudio, language='en_US')
                #result = recognizer.recognize_google(audio, language='ta-IN')
                text = text.lower()
                print('Your message:', format(text))

            except Exception as ex:
                print(ex)
    elif count ==3:
        for x in task:
            arm_move(x[0])
            print(x)
    arm_move(-200,70,160,0,0,90)
    time.sleep(3)
    arm_move(0,0,70,0,0,0)
    time.sleep(3)
    