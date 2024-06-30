import RPi.GPIO as gpio
import config as env
import json as JSON

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


def gpio_callback(client, pin):
    switch_id = env.switch_ids[env.gpio_input_pins.index(str(pin))]
    if switch_id is not None:
        print(f'Switch {switch_id} pressed',
              f'pin: {pin}', gpio.input(pin))
        client.publish(f'switch/{switch_id}/response', JSON.dumps(
            {'status': gpio.input(pin)}))
    else:
        print('Invalid switch_id')


def gpio_listner(client):
    for pin in env.gpio_input_pins:
        if pin is not None:
            gpio.setup(int(pin), gpio.IN)
            gpio.add_event_detect(int(pin), callback=lambda x: gpio_callback(
                client, x), bouncetime=200)
