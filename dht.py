import time
import board
import adafruit_dht
import os
from Adafruit_IO import Client
import sys

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT22(board.D26)
# Uncomment for DHT11
#sensor = adafruit_dht.DHT11(board.D4)

ADAFRUIT_USERNAME=os.getenv("MQTT_USERNAME")
ADAFRUIT_KEY=os.getenv("MQTT_KEY")

ioClient=Client(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
groupName="sensors"

if len(sys.argv) < 2:
    print("Usage: dht <rack>")
    sys.exit(1)

rack = sys.argv[1]
key = "sensors.data"


while True:
    try:
        # Print the values to the serial port
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        messageJsonTemplate = '''{{
            "rack": {rack},
            "temperature": {temp},
            "humidity: {humidity}
        }}'''

        message = messageJsonTemplate.format(rack=rack, temp=temperature_c, humidity=humidity)
        ioClient.send_data(key, message)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(3.0)