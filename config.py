import os
from dotenv import load_dotenv
load_dotenv()

mqtt_host = os.environ.get('MQTT_HOST')
mqtt_port = os.environ.get('MQTT_PORT', 1883)
sensor_id = os.environ.get('SENSOR_ID')
switch_ids = [
    os.environ.get('SWITCH_ID_1'),
    os.environ.get('SWITCH_ID_2'),
    os.environ.get('SWITCH_ID_3'),
    os.environ.get('SWITCH_ID_4'),
    os.environ.get('SWITCH_ID_5'),
    os.environ.get('SWITCH_ID_6')
]
