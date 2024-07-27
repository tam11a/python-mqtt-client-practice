import paho.mqtt.client as mqtt
import config as env
import json as JSON
import gpio
import dht as DHT
import threading
import ping
import connectivity


def on_switch_action(client, switch_id, payload):
    # print(f'Switch {switch_id} action > {payload.get("action")}')
    #
    #
    # Do something with the switch action
    action = payload.get('action')
    # db.getSwitchStatus(switch_id) is action:
    if gpio.buttons[env.switch_ids.index(switch_id)].is_pressed is action:
        client.publish(f'switch/{switch_id}/response', JSON.dumps(
            {'status': action}))
    else:
        gpio.gpio_action(switch_id, action)
    #
    #
    #
    # client.publish(f'switch/{switch_id}/response', JSON.dumps(
    #     {'status': payload.get('action')}))


def on_connect(client, userdata, flags, rc):
    print(f'Connected to {env.mqtt_host}')

    for switch_id in env.switch_ids:
        if switch_id is not None:
            client.subscribe(f'switch/{switch_id}/pending')


def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    if env.switchActionPattern.match(msg.topic):
        switchActionMatch = env.switchActionPattern.match(msg.topic)
        switch_id = switchActionMatch.group(1)
        payload = JSON.loads(msg.payload)
        on_switch_action(client, switch_id, payload)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(env.mqtt_host, int(env.mqtt_port), 60)

    # Threads Initialization

    thread_switch_from_app = threading.Thread(target=client.loop_forever)
    thread_dht = threading.Thread(
        target=DHT.dht_read, kwargs={'client': client})
    thread_gpio = threading.Thread(
        target=gpio.gpio_zero_listner, kwargs={'client': client})
    threan_room_toggle = threading.Thread(
        target=gpio.gpio_room_toggle, kwargs={'client': client})
    thread_ping = threading.Thread(
        target=ping.ping_server, kwargs={'client': client}
    )
    thread_connectivity = threading.Thread(
        target=connectivity.preview_connection, kwargs={'client': client}
    )

    thread_dht.start()
    thread_switch_from_app.start()
    thread_gpio.start()
    threan_room_toggle.start()
    thread_ping.start()
    thread_connectivity.start()
