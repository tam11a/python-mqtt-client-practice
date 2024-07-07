import json as JSON
from config import local_file_path, room_id


def getTemperature():
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    return data.get('temperature')


def getHumidity():
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    return data.get('humidity')


def setTemperature(temperature):
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    data['temperature'] = temperature
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def setHumidity(humidity):
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    data['humidity'] = humidity
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def getSwitchStatus(switch_id):
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    return data.get(f'switch_{switch_id}')


def setSwitchStatus(switch_id, status):
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    data[f'switch_{switch_id}'] = status
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def getRoomStatus():
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    return data.get(f'room_{room_id}')


def setRoomStatus(status):
    file = open(local_file_path, 'r')
    data = JSON.load(file)
    data[f'room_{room_id}'] = status
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True
