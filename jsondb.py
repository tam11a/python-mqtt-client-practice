import json
import os
import threading
from config import local_file_path as file_path

# Create a lock object
file_lock = threading.Lock()


def safe_write_json(data):
    temp_file_path = file_path + '.tmp'
    try:
        with file_lock:
            with open(temp_file_path, 'w') as temp_file:
                json.dump(data, temp_file)
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.rename(temp_file_path, file_path)
    except Exception as e:
        print(f"An error occurred [safe-write]: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def safe_read_json():
    with file_lock:
        if not os.path.exists():
            return {}
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"An error occurred [safe-read]: {e}")
            return {}
