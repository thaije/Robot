# This script uses software pwd on a sne73 chip to
# drive two dc motors
# Speed of the DC motors is based on average voltage
# Low duty cycle is short pulses with short pauses inbetween (low aver. voltage)
# High duty cycle is long pulses with long pauses inbetween (high aver. voltage)
# Max duty cycle is 100

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

class Motor:

    def __init__(self, pinForward, pinBackward, pinControl):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinControl = pinControl
        GPIO.setup(self.pinForward, GPIO.OUT)
        GPIO.setup(self.pinBackward, GPIO.OUT)
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pinForward, 100)
        self.pwm_backward = GPIO.PWM(self.pinBackward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
        GPIO.output(self.pinControl, GPIO.HIGH)

    def forward(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_backward.ChangeDutyCycle(0)
        self.pwm_forward.ChangeDutyCycle(speed)

    def backward(self, speed):
        """ pinBackward is the forward Pin, so wwiringpi.pwmWrite(18,0)
        wiringpi.pwmWrite(13,0)e change its duty cycle according to speed. """

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(speed)

    def stop(self):
        """ Set the duty cycle of both control pins to zero to
        stop the motor. """

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)



#######################################
# Methods to move the wheels
#######################################

# Move in a direction forward/backward
# s = speed [-99, 99], minus = backward
def move(s):
    s = clamp(s, -99, 99)
    if s < 0:
        motor1.backward(-s)
        motor2.backward(-s)
    elif s > 0:
        motor1.forward(s)
        motor2.forward(s)


# stop turning of motors
def stop():
    motor1.stop()
    motor2.stop()


# turn the robot
# r = direction, r > 0=leftturn, r < 0=rightturn
# s = speed [1,99]
def turn(r,s):
    s = clamp(s, 0, 99)

    # turn left
    if r > 0:
        motor1.backward(s)
        motor2.forward(s)
    elif r < 0:
        motor1.forward(s)
        motor2.backward(s)

# Limit a value to a min and max
def clamp(n, minN, maxN):
    return max(min(maxN, n), minN)


def cleanup():
    stop()
    GPIO.cleanup()


# Test the motors
def test():
    motor1.forward(100)
    sleep(5)
    motor1.backward(40)
    sleep(2)
    motor1.stop()
    cleanup()



# initiliase motors
# motor1 = sne73 right side
# motor2 = sne73 left side
motor1 = Motor(16, 22, 18)
print "DC motor 1 online"
motor2 = Motor(23, 19, 21)
print "DC motor 2 online"


#test()