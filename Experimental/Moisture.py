
import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the sensor module
sensor_vcc_pin = 2   # 3.3V pin on Raspberry Pi
sensor_gnd_pin = 6   # GND pin on Raspberry Pi
sensor_d0_pin = 17   # GPIO pin for D0 on Raspberry Pi
sensor_a0_pin = 4    # Analog input pin for A0 on Raspberry Pi

# Set up the GPIO pins for the sensor module
GPIO.setup(sensor_vcc_pin, GPIO.OUT)
GPIO.setup(sensor_gnd_pin, GPIO.OUT)
GPIO.setup(sensor_d0_pin, GPIO.IN)
GPIO.setup(sensor_a0_pin, GPIO.IN)

# Set up the sensor module
GPIO.output(sensor_vcc_pin, GPIO.HIGH)  # Turn on power to the sensor module
GPIO.output(sensor_gnd_pin, GPIO.LOW)   # Connect GND to the sensor module

# Read the analog output from the sensor module and calculate percentage
while True:
    soil_moisture_value = GPIO.input(sensor_d0_pin)
    print("Soil Moisture Value:", soil_moisture_value)
    time.sleep(0.5)
