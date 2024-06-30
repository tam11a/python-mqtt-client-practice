import paho.mqtt.client as mqtt
import config as env
import json as JSON
import gpio
import dht as DHT
import threading


def on_switch_action(client, switch_id, payload):
    # print(f'Switch {switch_id} action > {payload.get("action")}')
    #
    #
    # Do something with the switch action
    gpio.gpio_action(switch_id, payload.get('action'))
    #
    #
    #
    client.publish(f'switch/{switch_id}/response', JSON.dumps(
        {'status': payload.get('action')}))


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

    thread_switch = threading.Thread(target=client.loop_forever)
    thread_dht = threading.Thread(
        target=DHT.dht_read, kwargs={'client': client})

    thread_dht.start()
    thread_switch.start()
