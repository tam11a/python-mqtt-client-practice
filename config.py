import re
import os
from dotenv import load_dotenv
load_dotenv()

# ENVIRONMENT VARIABLES
# Path: .env

mqtt_host = os.environ.get('MQTT_HOST')
mqtt_port = os.environ.get('MQTT_PORT', 1883)

sensor_id = os.environ.get('SENSOR_ID')
sensor_pin = os.environ.get('SENSOR_PIN')

switch_ids = [
    os.environ.get('SWITCH_ID_1'),
    os.environ.get('SWITCH_ID_2'),
    os.environ.get('SWITCH_ID_3'),
    os.environ.get('SWITCH_ID_4'),
    os.environ.get('SWITCH_ID_5'),
    os.environ.get('SWITCH_ID_6')
]
gpio_pins = [
    os.environ.get('GPIO_PIN_1'),
    os.environ.get('GPIO_PIN_2'),
    os.environ.get('GPIO_PIN_3'),
    os.environ.get('GPIO_PIN_4'),
    os.environ.get('GPIO_PIN_5'),
    os.environ.get('GPIO_PIN_6')
]
gpio_input_pins = [
    os.environ.get('GPIO_PIN_1_INPUT'),
    os.environ.get('GPIO_PIN_2_INPUT'),
    os.environ.get('GPIO_PIN_3_INPUT'),
    os.environ.get('GPIO_PIN_4_INPUT'),
    os.environ.get('GPIO_PIN_5_INPUT'),
    os.environ.get('GPIO_PIN_6_INPUT')
]


# Patterns

switchActionPattern = re.compile(r'switch/(\d+)/pending')
