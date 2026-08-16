import json
import os
import time

LOG_FILE = "zara_gui_log.jsonl"
STATUS_FILE = "zara_gui_status.json"

def send_to_gui(sender, message):
    try:
        data = {
            "time": time.time(),
            "sender": sender,
            "message": message
        }

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(data) + "\n")

    except:
        pass

def send_status_to_gui(status, color="#00FF66", message=""):
    try:
        data = {
            "status": status,
            "color": color,
            "message": message
        }

        with open(STATUS_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file)

    except:
        pass