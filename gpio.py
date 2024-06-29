import RPi.GPIO as gpio
import config as env

# Setup GPIO pins
gpio.setmode(gpio.BCM)

for pin in env.gpio_pins:
    if pin is not None:
        gpio.setup(int(pin), gpio.OUT)


def gpio_action(switch_id, action):
    gpio_pin = int(env.gpio_pins[env.switch_ids.index(switch_id)])
    if gpio_pin is not None:
        if action == True:
            gpio.output(gpio_pin, gpio.HIGH)
        elif action == False:
            gpio.output(gpio_pin, gpio.LOW)
        else:
            print('Invalid action')
    else:
        print('Invalid switch_id')
