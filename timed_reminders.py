import json
import os
import datetime

TIMED_REMINDERS_FILE = "timed_reminders.json"

def load_timed_reminders():
    if not os.path.exists(TIMED_REMINDERS_FILE):
        return []

    with open(TIMED_REMINDERS_FILE, "r") as file:
        return json.load(file)

def save_timed_reminders(reminders):
    with open(TIMED_REMINDERS_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def add_timed_reminder(task, time_text):
    reminders = load_timed_reminders()

    reminders.append({
        "task": task,
        "time": time_text,
        "done": False
    })

    save_timed_reminders(reminders)

def get_timed_reminders():
    return load_timed_reminders()

def clear_timed_reminders():
    save_timed_reminders([])

def mark_reminder_done(index):
    reminders = load_timed_reminders()

    if 0 <= index < len(reminders):
        reminders[index]["done"] = True
        save_timed_reminders(reminders)

def check_due_reminders():
    reminders = load_timed_reminders()
    current_time = datetime.datetime.now().strftime("%I:%M %p").lower()

    due = []

    for index, reminder in enumerate(reminders):
        if not reminder["done"] and reminder["time"].lower() == current_time:
            due.append((index, reminder["task"]))

    return due