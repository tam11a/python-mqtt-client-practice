import board
import adafruit_dht
import config as env
import json as JSON
import time

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)


def dht_read(client):
    print('Reading DHT sensor')
    print(f'Sensor ID: {env.sensor_id}')
    print(f'Sensor Pin: {env.sensor_pin}')
    print(client)
    if env.sensor_id is None:
        raise Exception('SENSOR_ID is not set')
    while True:
        try:
            print(dhtDevice, dhtDevice.temperature, dhtDevice.humidity)
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity

            print({'temperature_c': temperature_c,
                   'temperature_f': temperature_f, 'humidity': humidity})

            client.publish(f'sensor/{env.sensor_id}/live', JSON.dumps(
                {'ref': env.sensor_id, 'temp': temperature_c, 'hum': humidity}))

            time.sleep(1)  # 5 seconds sleep

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2)
            continue

        except Exception as error:
            print(error)
            raise error
