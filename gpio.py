import RPi.GPIO as gpio
import config as env
import json as JSON
import db

prev_input = {pin: db.getSwitchStatus(pin) for pin in env.gpio_input_pins}
toggle_state = 0

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
            print(f'[Switch {switch_id}][Pin {gpio_pin}] turned ON', action)
        elif action == False:
            gpio.output(gpio_pin, gpio.LOW)
            print(f'[Switch {switch_id}][Pin {gpio_pin}] turned OFF', action)
        else:
            print('Invalid action')
    else:
        print('Invalid switch_id')


def gpio_callback(client, pin):
    switch_id = env.switch_ids[env.gpio_input_pins.index(str(pin))]
    if switch_id is not None:
        print(f'Switch {switch_id} pressed',
              f'pin: {pin}', gpio.input(pin))
        db.setSwitchStatus(switch_id, gpio.input(pin))
        client.publish(f'switch/{switch_id}/response', JSON.dumps(
            {'status': gpio.input(pin)}))
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
                    # print('[GPIO LISTNER]', input_state, prev_input[pin],
                    #       pin, env.switch_ids[env.gpio_input_pins.index(pin)])
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


def gpio_room_toggle(client):
    if env.toggle_pin is not None:
        try:
            gpio.setup(int(env.toggle_pin), gpio.IN)
            while True:
                input_state = gpio.input(int(env.toggle_pin))
                if input_state != toggle_state:
                    toggle_state = input_state

                    # Save to Local DB
                    db.setRoomStatus(env.room_id, input_state)

                    print(f'Toggle pressed', True if input_state == 1 else False)
                    client.publish(f'room/{env.room_id}/toggle',
                                   JSON.dumps({'toggle': True if input_state == 1 else False}))
        except Exception as error:
            print(f'Error setting up pin {env.toggle_pin}: {error}')
    else:
        print('Toggle pin is not set')
