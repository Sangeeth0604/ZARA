import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)

def remember(key, value):
    memory = load_memory()
    memory[key.lower()] = value
    save_memory(memory)

def recall(key):
    memory = load_memory()
    return memory.get(key.lower())

def delete_memory(key):
    memory = load_memory()
    key = key.lower()

    if key in memory:
        del memory[key]
        save_memory(memory)
        return True

    return False

def clear_all_memory():
    save_memory({})

def search_memory(keyword):
    memory = load_memory()
    results = {}

    for key, value in memory.items():
        if keyword.lower() in key.lower() or keyword.lower() in str(value).lower():
            results[key] = value

    return results