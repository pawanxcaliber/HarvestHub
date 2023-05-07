import RPi.GPIO as GPIO
import time
 
# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN) # Moisture sensor connected to GPIO 17
GPIO.setup(23, GPIO.OUT) # Relay module connected to GPIO 23
 
# Define a function to check moisture level and control the motor
def check_moisture():
    if GPIO.input(17) == 0: # Moisture level is low, turn on motor
        GPIO.output(23, GPIO.HIGH) # Turn on relay
        print("Moisture level is low. Motor is on.")
    else: # Moisture level is high, turn off motor
        GPIO.output(23, GPIO.LOW) # Turn off relay
        print("Moisture level is high. Motor is off.")
 
# Run the function in a loop
while True:
    check_moisture()
    time.sleep(5) # Wait for 5 seconds before checking again
