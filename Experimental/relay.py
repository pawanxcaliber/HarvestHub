import RPi.GPIO as GPIO
import time

# set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

# define function to turn on motor
def turn_on_motor():
    GPIO.output(23, GPIO.LOW)

# define function to turn off motor
def turn_off_motor():
    GPIO.output(23, GPIO.HIGH)

# main program
try:
    # turn on motor for 5 seconds
    turn_on_motor()
    time.sleep(5)
    
    # turn off motor and wait for 2 seconds
    turn_off_motor()
    time.sleep(2)
    
    # turn on motor for 5 seconds again
    turn_on_motor()
    time.sleep(5)
    
    # turn off motor and clean up GPIO
    turn_off_motor()
    GPIO.cleanup()
    
except KeyboardInterrupt:
    # clean up GPIO if program is interrupted
    GPIO.cleanup()
