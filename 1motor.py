import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# arm initial position global declaration
global servo1_initial_position
global servo2_initial_position
global servo3_initial_position
global stepper_motor_main_initial_position
global stepper_motor_1_initial_position
global stepper_motor_2_initial_position
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
# sensor global declaration
global UltraSonic_pins
global arm_initail_position_list
global task
# Arm and motor pins numbers declaration
servo_pin = [7,11,13]
stepper_motor_1_pins = [7, 11, 13, 15]
stepper_motor_2_pins = [ 7, 11, 13, 15]
stepper_motor_main_pins = [ 7, 11, 13, 15]

#servo motor pins
GPIO.setup(servo_pin[0], GPIO.OUT)
GPIO.setup(servo_pin[1], GPIO.OUT)
GPIO.setup(servo_pin[2], GPIO.OUT)
servo1 = GPIO.PWM(servo_pin[0], 50)
servo2 = GPIO.PWM(servo_pin[1], 50)
servo3 = GPIO.PWM(servo_pin[2], 50)
servo1.start(0)
servo2.start(0)
servo3.start(0)

task = []

global halfstep_seq
global hello_seq
global stepper_motor_main_seq
stepper_motor_main_seq = [
  [1, 0, 1, 0],
  [0, 1, 1, 0],
  [0, 1, 0, 1],
  [1, 0, 0, 1]
]
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

class Move:
    def __init__(self):
        self.move_arm()
    def arm_move(servo1_angle, servo2_angle, Stepper_motor1_angle, Stepper_motor2_angle,
                 servo3_angle, arm_speed):
        while True:
            change_stepper_motor1 = round(1.4222222222 * Stepper_motor1_angle)
            change_stepper_motor2 = round(1.4222222222 * Stepper_motor2_angle)
            if present_servo1_position != servo1_angle:
                servo1.ChangeDutyCycle(2 + (servo1_angle / 18))
                present_servo1_position = servo1_angle
            if present_servo2_position != servo2_angle:
                servo1.ChangeDutyCycle(2 + (servo2_angle / 18))
                present_servo2_position = servo2_angle
            if present_servo3_position != servo3_angle:
                servo1.ChangeDutyCycle(2 + (servo3_angle / 18))
                present_servo3_position = servo3_angle
            if present_stepper_motor1_position != change_stepper_motor1:
                if change_stepper_motor1 > present_stepper_motor1_position:
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(stepper_motor_1_pins[pin], halfstep_seq[halfstep][pin])
                    present_stepper_motor1_position += 1
                else:
                    for halfstep in range(7, 0, -1):
                        for pin in range(4):
                            GPIO.output(stepper_motor_1_pins[pin], halfstep_seq[halfstep][pin])
                    present_stepper_motor1_position -= 1
            if present_stepper_motor2_position != change_stepper_motor2:
                if change_stepper_motor2 > present_stepper_motor2_position:
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(stepper_motor_2_pins[pin], halfstep_seq[halfstep][pin])
                    present_stepper_motor2_position +=1

                else:
                    for halfstep in range(8):
                        for pin in range(4):
                            GPIO.output(stepper_motor_2_pins[pin], halfstep_seq[halfstep][pin])
                    present_stepper_motor2_position -= 1
            if present_stepper_motor1_position == change_stepper_motor1 and present_stepper_motor2_position == change_stepper_motor2 :
               # return True
                break
    def arm_initial_position(self):
        with open(" ") as arm_initial_position_file:
            arm_initail_position_list.append(arm_initial_position_file.readline().split(","))
        self.arm_move(int(arm_initail_position_list[0]),int(arm_initail_position_list[1]),int(arm_initail_position_list[2]),int(arm_initail_position_list[3]),int(arm_initail_position_list[4]),int(arm_initail_position_list[5]))
    def say_move(self,file_name,speed):
        with open(file_name + ".txt") as arm_file:
            for x_file in arm_file:
                task = x_file.readline().split(",")
                self.arm_move(int(task[0]),int(task[1]),int(task[2]),int(task[3]),int(task[4]),int(task[5]),speed)



