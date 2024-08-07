import jsondb
from config import room_id


def getTemperature():
    try:
        return jsondb.safe_read_json().get('temperature')
    except:
        return None


def getHumidity():
    try:
        return jsondb.safe_read_json().get('humidity')
    except:
        return None


def setTemperature(temperature):
    try:
        data = jsondb.safe_read_json()
        data['temperature'] = temperature
        jsondb.safe_write_json(data)
        return True
    except Exception as e:
        print(f"An error occurred [set-temperature]: {e}")
        return False


def setHumidity(humidity):
    try:
        data = jsondb.safe_read_json()
        data['humidity'] = humidity
        jsondb.safe_write_json(data)
        return True
    except Exception as e:
        print(f"An error occurred [set-humidity]: {e}")
        return False


def getSwitchStatus(switch_id):
    try:
        return jsondb.safe_read_json().get(f'switch_{switch_id}')
    except:
        return None


def setSwitchStatus(switch_id, status):
    try:
        data = jsondb.safe_read_json()
        data[f'switch_{switch_id}'] = status
        jsondb.safe_write_json(data)
        return True
    except Exception as e:
        print(f"An error occurred [set-switch-status]: {e}")
        return False


def getRoomStatus():
    try:
        return jsondb.safe_read_json().get(f'room_{room_id}')
    except:
        return None


def setRoomStatus(status):
    try:
        data = jsondb.safe_read_json()
        data[f'room_{room_id}'] = status
        jsondb.safe_write_json(data)
        return True
    except Exception as e:
        print(f"An error occurred [set-room-status]: {e}")
        return False
