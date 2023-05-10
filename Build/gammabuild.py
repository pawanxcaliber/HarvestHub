import RPi.GPIO as GPIO
import time
import sqlite3
from twilio.rest import Client # https://console.twilio.com/?frameUrl=%2Fconsole%3Fx-target-region%3Dus1&newCustomer=true

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
    if GPIO.input(17) == 0: # Moisture level is high, turn off motor
        GPIO.output(23, GPIO.HIGH) # Turn off relay
        motor_status = 'off'
        print("Moisture level is high. Motor is off.")
        send_sms('Motor off') # Send SMS notification
    else: # Moisture level is low, turn on motor
        GPIO.output(23, GPIO.LOW) # Turn on relay
        motor_status = 'on'
        print("Moisture level is low. Motor is on.")
        send_sms('Motor on') # Send SMS notification

    # Log data into database
    conn.execute("INSERT INTO irrigation_data (moisture, motor_status) VALUES (?, ?)", (GPIO.input(17), motor_status))
    conn.commit()

    # Send 10 readings from database to phone number every 10 readings
    if get_data_count() % 10 == 0:
        data = get_last_n_readings(10)
        send_sms('Irrigation system data: ' + str(data)) # Send SMS with data

# Define a function to send SMS notification
def send_sms(message):
    # Replace the placeholders with your Twilio account SID, auth token, and phone numbers
    account_sid = 'AC4faa86624345646aaed13b90c247941a'
    auth_token = '16b6f9d7cdc3ab1dd8be77ef6877905a'
    from_number = '+12706068163'
    to_number = '+918073984203'

    # Set up the Twilio client and send the SMS
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=from_number, to=to_number)

# Define a function to get the number of data points in the database
def get_data_count():
    cursor = conn.execute("SELECT COUNT(*) FROM irrigation_data")
    count = cursor.fetchone()[0]
    return count

# Define a function to get the last n readings from the database
def get_last_n_readings(n):
    cursor = conn.execute("SELECT * FROM irrigation_data ORDER BY id DESC LIMIT ?", (n,))
    data = cursor.fetchall()
    return data

# Run the function in a loop
while True:
    check_moisture()
    time.sleep(1) # Wait for 5 seconds before checking again

# Close the database connection
conn.close()


