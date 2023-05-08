import RPi.GPIO as GPIO
import time
import sqlite3
 
# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN) # Moisture sensor connected to GPIO 17
GPIO.setup(23, GPIO.OUT) # Relay module connected to GPIO 23
 
# Create a connection to the database
conn = sqlite3.connect('irrigation_system.db')
 
# Create a table to store moisture and motor status data
conn.execute('''CREATE TABLE IF NOT EXISTS irrigation_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             moisture INTEGER,
             motor_status TEXT)''')
 
# Define a function to check moisture level and control the motor
def check_moisture():
    if GPIO.input(17) == 0: # Moisture level is low, turn on motor
        GPIO.output(23, GPIO.HIGH) # Turn on relay
        motor_status = 'on'
        print("Moisture level is high. Motor is off.")
    else: # Moisture level is high, turn off motor
        GPIO.output(23, GPIO.LOW) # Turn off relay
        motor_status = 'off'
        print("Moisture level is low. Motor is on.")
 
    # Log data into database
    conn.execute("INSERT INTO irrigation_data (moisture, motor_status) VALUES (?, ?)", (GPIO.input(17), motor_status))
    conn.commit()
 
# Run the function in a loop
while True:
    check_moisture()
    time.sleep(5) # Wait for 5 seconds before checking again
 
# Close the database connection
conn.close()
