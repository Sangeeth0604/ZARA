import json
import os

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []

    with open(REMINDERS_FILE, "r") as file:
        return json.load(file)

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def add_reminder(reminder):
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)

def get_reminders():
    return load_reminders()

def clear_reminders():
    save_reminders([])