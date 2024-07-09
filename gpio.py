import RPi.GPIO as gpio
import lgpio
import config as env
import json as JSON
import db
from datetime import datetime
import time
from gpiozero import Button

pending_input = {pin: {
    'state': db.getSwitchStatus(env.switch_ids[env.gpio_input_pins.index(pin)]),
    'timestamp': datetime.now()
} for pin in env.gpio_input_pins}

prev_input = {pin: db.getSwitchStatus(env.switch_ids[env.gpio_input_pins.index(
    pin)]) for pin in env.gpio_input_pins}

# Setup GPIO pins
gpio.setmode(gpio.BCM)

for pin in env.gpio_pins:
    if pin is not None:
        print('Setting up pin', pin, 'as output', flush=True)
        gpio.setup(int(pin), gpio.OUT)


def gpio_action(switch_id, action):
    gpio_pin = int(env.gpio_pins[env.switch_ids.index(switch_id)])
    if gpio_pin is not None:
        if action == True:
            gpio.output(gpio_pin, gpio.HIGH)
            print(f'[Switch {switch_id}][Pin {gpio_pin}] turned ON', action)
            pending_input[str(gpio_pin)] = {
                'state': 1, 'timestamp': datetime.now()}

        elif action == False:
            gpio.output(gpio_pin, gpio.LOW)
            print(f'[Switch {switch_id}][Pin {gpio_pin}] turned OFF', action)
            pending_input[str(gpio_pin)] = {
                'state': 0, 'timestamp': datetime.now()}
        else:
            print('Invalid action')
    else:
        print('Invalid switch_id')


def gpio_listner(client):
    for pin in env.gpio_input_pins:
        if pin is not None:
            try:
                gpio.setup(int(pin), gpio.IN)  # pull_up_down=gpio.PUD_DOWN
                # gpio.add_event_detect(int(pin), edge=gpio.BOTH, callback=lambda x: gpio_callback(
                #     client, x), bouncetime=200)
            except Exception as error:
                print(f'Error setting up pin {pin}: {error}')
                continue
    while True:
        for pin in env.gpio_input_pins:
            if pin is not None:
                try:
                    input_state = gpio.input(int(pin))
                    temp_pin = str(env.gpio_pins[env.gpio_input_pins.index(
                        pin)])
                    # pending_input[temp_pin] == None or (datetime.now() - pending_input[temp_pin].timestamp).total_seconds > 10
                    print('[GPIO LISTNER]', pending_input[temp_pin]
                          is None or input_state != prev_input[pin])
                    # if pending_input[temp_pin] is None or (datetime.now() - pending_input[temp_pin]['timestamp']).total_seconds > 10 or
                    if input_state != prev_input[pin]:
                        prev_input[pin] = input_state
                        switch_id = env.switch_ids[env.gpio_input_pins.index(
                            pin)]

                        # Save to Local DB
                        db.setSwitchStatus(switch_id, input_state)

                        print(f'Switch {switch_id} pressed',
                              f'pin: {pin}', True if input_state == 0 else False)

                        client.publish(
                            f'switch/{switch_id}/response', JSON.dumps({'status': True if input_state == 0 else False}))
                        # gpio.setup(int(pin), gpio.IN, pull_up_down=gpio.PUD_DOWN)
                        # gpio.add_event_detect(int(pin), edge=gpio.BOTH, callback=lambda x: gpio_callback(
                        #     client, x), bouncetime=200)
                except Exception as error:
                    print(f'Error setting up pin {pin}: {error}')
                    continue


def gpio_event_listner(client):
    for pin in env.gpio_input_pins:
        if pin is not None:
            try:
                gpio.setup(int(pin), gpio.IN, gpio.PUD_UP)
                gpio.add_event_detect(
                    int(pin), lgpio.FALLING_EDGE, callback=lambda: gpio_zero_callback(client, pin, True))
                gpio.add_event_detect(
                    int(pin), lgpio.RISING_EDGE, callback=lambda: gpio_zero_callback(client, pin, False))
            except Exception as error:
                print(f'Error setting up pin {pin}: {error}')
                continue
    while True:
        time.sleep(1)


def gpio_zero_callback(client, pin, status):
    print('[GPIO ZERO CALLBACK]', pin, status)
    switch_id = env.switch_ids[env.gpio_input_pins.index(str(pin))]
    if switch_id is not None:
        print(f'Switch {switch_id} pressed',
              f'pin: {pin}', status)
        # db.setSwitchStatus(switch_id, status)
        # client.publish(f'switch/{switch_id}/response', JSON.dumps(
        #     {'status': status}))
    else:
        print('Invalid switch_id')


def gpio_zero_listner(client):
    for pin in env.gpio_input_pins:
        if pin is not None:
            try:
                button = Button(int(pin), pull_up=False)
                button.when_pressed = lambda: gpio_zero_callback(
                    client, pin, True)
                button.when_released = lambda: gpio_zero_callback(
                    client, pin, False)
            except Exception as error:
                print(f'Error setting up pin {pin}: {error}')
                continue
    while True:
        time.sleep(1)


def gpio_room_toggle(client):
    if env.toggle_pin is not None:
        try:
            gpio.setup(int(env.toggle_pin), gpio.IN)
            while True:
                input_state = gpio.input(int(env.toggle_pin))
                if input_state != db.getRoomStatus():
                    # Save to Local DB
                    db.setRoomStatus(input_state)

                    print(f'Toggle pressed', True if input_state == 1 else False)
                    client.publish(f'room/{env.room_id}/toggle',
                                   JSON.dumps({'toggle': True if input_state == 1 else False}))
        except Exception as error:
            print(f'Error setting up pin {env.toggle_pin}: {error}')
    else:
        print('Toggle pin is not set')
