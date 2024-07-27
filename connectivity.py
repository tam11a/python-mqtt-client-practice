import config
import time
import RPi.GPIO as gpio
import db


def preview_connection(client):

    light_status = 0

    while True:
        if client.is_connected() is False:
            if config.manual_green_pin is not None:
                gpio.output(int(config.manual_green_pin), gpio.LOW
                            if light_status == 1 else gpio.HIGH)
            light_status = 1 if light_status == 0 else 0
        else:
            if config.manual_red_pin is not None and config.manual_green_pin is not None:
                if db.getRoomStatus():
                    gpio.output(int(config.manual_red_pin), gpio.LOW)
                    gpio.output(int(config.manual_green_pin), gpio.HIGH)
                else:
                    gpio.output(int(config.manual_red_pin), gpio.HIGH)
                    gpio.output(int(config.manual_green_pin), gpio.LOW)
        time.sleep(1)
