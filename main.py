import paho.mqtt.client as mqtt
import config as env


def on_connect(client, userdata, flags, rc):
    print(f'Connected to {env.mqtt_host}')

    for switch_id in env.switch_ids:
        if switch_id is not None:
            client.subscribe(f'switch/{switch_id}/action')


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(env.mqtt_host, int(env.mqtt_port), 60)
client.loop_forever()
