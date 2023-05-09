import RPi.GPIO as GPIO
import time
import sqlite3
import xml.etree.ElementTree as ET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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

    # If 10 readings have been recorded, convert database to XML and email it
    if conn.execute("SELECT COUNT(*) FROM irrigation_data").fetchone()[0] % 10 == 0:
        # Convert database to XML
        root = ET.Element("irrigation_data")
        for row in conn.execute("SELECT * FROM irrigation_data"):
            item = ET.SubElement(root, "item")
            item.set("id", str(row[0]))
            item.set("timestamp", str(row[1]))
            item.set("moisture", str(row[2]))
            item.set("motor_status", row[3])
        xml_data = ET.tostring(root)

        # Email the XML data
        msg = MIMEMultipart()
        msg['From'] = 'sender_email_address'
        msg['To'] = 'pawanmkolachippu@gmail.com'
        msg['Subject'] = 'Irrigation System Data'
        body = 'Please find attached the irrigation system data for the last 10 readings.'
        msg.attach(MIMEText(body, 'plain'))
        attachment = MIMEApplication(xml_data, _subtype='xml', _encoder=None)
        attachment.add_header('content-disposition', 'attachment', filename='irrigation_data.xml')
        msg.attach(attachment)

        # Send the email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'sender_email_address'
        smtp_password = 'sender_email_password'
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

# Run the function in a loop
while True:
    check_moisture()
    time.sleep(5) # Wait for 5 seconds before checking again

# Close the database connection
conn.close()
