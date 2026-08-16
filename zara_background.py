import main
import subprocess
import time
import os

def is_wakeup_command(command):
    command = command.lower()
    wake_words = [
        "wake up zara",
        "wake up sara",
        "wake up tara",
        "wakeup zara",
        "wakeup sara",
        "wakeup tara",
        "hey zara",
        "hello zara",
        "zara wake up",
        "zara"
    ]

    return any(word in command for word in wake_words)

def is_close_command(command):
    command = command.lower()

    close_words = [
        "close zara",
        "close sara",
        "close tara"
    ]

    return any(word in command for word in close_words)

def is_shutdown_command(command):
    command = command.lower()

    shutdown_words = [
        "shutdown zara",
        "shutdown sara",
        "shutdown tara"
    ]

    return any(word in command for word in shutdown_words)

active = False
gui_process = None

def open_working_gui():
    global gui_process

    if gui_process is None or gui_process.poll() is not None:
        gui_process = subprocess.Popen(["python", "zara_working_gui.py"])

def close_working_gui():
    global gui_process

    if gui_process is not None:
        gui_process.terminate()
        gui_process = None

def background_loop():
    global active

    print("ZARA Background is running...")
    print("Say 'zara wakeup' to activate.")
    print("Say 'zara close' to sleep.")
    print("Say 'zara shutdown' to exit completely.")

    while True:
        command = main.listen()

        if command == "":
            continue

        if is_shutdown_command(command):
            main.speak("Shutting down ZARA.")
            close_working_gui()
            break

        if not active:
            if is_wakeup_command(command):
                active = True
                open_working_gui()
                main.speak("Yes Sangeeth, I am ready.")
            else:
                continue

        else:
            if is_close_command(command):
                main.speak("Going silent.")
                close_working_gui()
                active = False
                continue

            main.run_zara(command)

if __name__ == "__main__":
    background_loop()