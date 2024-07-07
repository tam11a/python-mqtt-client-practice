import json as JSON
from config import local_file_path, room_id

with open(local_file_path, "r+") as file:
    try:
        data = JSON.load(file)
    except:
        print(file)
        # file.write({})


def getTemperature():
    try:
        file = open(local_file_path, 'r')
        data = JSON.load(file)
        return data.get('temperature')
    except:
        return None


def getHumidity():
    try:
        file = open(local_file_path, 'r')
        data = JSON.load(file)
        return data.get('humidity')
    except:
        return None


def setTemperature(temperature):
    file = open(local_file_path, 'r+')
    data = JSON.load(file)
    data['temperature'] = temperature
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def setHumidity(humidity):
    file = open(local_file_path, 'r+')
    data = JSON.load(file)
    data['humidity'] = humidity
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def getSwitchStatus(switch_id):
    try:
        file = open(local_file_path, 'r')
        data = JSON.load(file)
        return data.get(f'switch_{switch_id}')
    except:
        return None


def setSwitchStatus(switch_id, status):
    file = open(local_file_path, 'r+')
    data = JSON.load(file)
    data[f'switch_{switch_id}'] = status
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True


def getRoomStatus():
    try:
        file = open(local_file_path, 'r')
        data = JSON.load(file)
        return data.get(f'room_{room_id}')
    except:
        return None


def setRoomStatus(status):
    file = open(local_file_path, 'r+')
    data = JSON.load(file)
    data[f'room_{room_id}'] = status
    file = open(local_file_path, 'w')
    JSON.dump(data, file)
    file.close()
    return True
