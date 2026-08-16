WAKE_WORDS = [
    "hey zara",
    "hello zara",
    "zara"
]

def is_wake_word(command):
    command = command.lower().strip()

    for word in WAKE_WORDS:
        if word == command:
            return True

    return False