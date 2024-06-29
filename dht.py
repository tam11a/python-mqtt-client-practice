import board
import Adafruit_DHT
import RPi.GPIO as gpio
import config as env
import json as JSON

# Initialize the DHT device, with data pin connected to:
dhtDevice = Adafruit_DHT.DHT22(board.D4, use_pulseio=False)


def dht_read(client):
    if env.sensor_id is None:
        raise Exception('SENSOR_ID is not set')
    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print({'temperature_c': temperature_c,
                   'temperature_f': temperature_f, 'humidity': humidity})
            client.publish(f'sensor/{env.sensor_id}/live', JSON.dumps(
                {'ref': env.sensor_id, 'temp': temperature_c, 'hum': humidity}))
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            return None
        except Exception as error:
            dhtDevice.exit()
            raise error
