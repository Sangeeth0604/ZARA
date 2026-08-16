import json

with open("config.json", "r", encoding="utf-8") as file:
    CONFIG = json.load(file)

USER_NAME = CONFIG["user_name"]
ASSISTANT_NAME = CONFIG["assistant_name"]
WAKE_WORD = CONFIG["wake_word"]
VOICE_RATE = CONFIG["voice_rate"]
VOICE_ENABLED = CONFIG["voice_enabled"]