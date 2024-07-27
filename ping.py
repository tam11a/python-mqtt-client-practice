import config
import json as JSON
import time


def ping_server(client):
    while True:
        client.publish(f'ping/{config.room_id}',
                       JSON.dumps({'status': 'ping'}))
        time.sleep(5)
