import config
import json as JSON
import time
import RPi.GPIO as gpio


def ping_server(client):

    light_status = 0

    while True:
        if client.is_connected() is False:
            if config.manual_green_pin is not None:
                gpio.output(int(config.manual_green_pin), gpio.LOW
                            if light_status == 1 else gpio.HIGH)
            light_status = 1 if light_status == 0 else 0
        else:
            client.publish(f'ping/{config.room_id}',
                           JSON.dumps({'status': 'ping'}))
        time.sleep(5)
