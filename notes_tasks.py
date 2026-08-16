import json
import os

NOTES_FILE = "notes.json"
TASKS_FILE = "tasks.json"

def load_data(file_name):
    if not os.path.exists(file_name):
        return []

    with open(file_name, "r") as file:
        return json.load(file)

def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

def add_note(note):
    notes = load_data(NOTES_FILE)
    notes.append(note)
    save_data(NOTES_FILE, notes)

def get_notes():
    return load_data(NOTES_FILE)

def add_task(task):
    tasks = load_data(TASKS_FILE)
    tasks.append(task)
    save_data(TASKS_FILE, tasks)

def get_tasks():
    return load_data(TASKS_FILE)

def clear_tasks():
    save_data(TASKS_FILE, [])