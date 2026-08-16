import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import random
import pyautogui
import psutil
import requests
import wikipedia

from ai_brain import ask_ai
from memory import (
    remember,
    recall,
    load_memory,
    save_memory,
    delete_memory,
    clear_all_memory,
    search_memory
)
from notes_tasks import add_note, get_notes, add_task, get_tasks, clear_tasks
from gui_bridge import send_to_gui, send_status_to_gui
from reminders import add_reminder, get_reminders, clear_reminders
from vision_ai import analyze_screen
from pdf_reader import summarize_latest_pdf
from file_assistant import (
    get_desktop_path,
    get_downloads_path,
    list_files,
    find_files_by_keyword,
    find_pdf_files,
    open_file
)
from face_login import register_face, verify_face
from coding_assistant import (
    explain_code,
    fix_error,
    optimize_code,
    generate_test_cases
)
from timed_reminders import (
    add_timed_reminder,
    get_timed_reminders,
    clear_timed_reminders,
    check_due_reminders,
    mark_reminder_done
)
from wake_word import is_wake_word
from config import *

CONVERSATION_MODE = False

def speak(text):
    print(f"{ASSISTANT_NAME}:", text)
    try:
        send_to_gui("ZARA", text)
    except:
        pass
    send_status_to_gui("Responding", "#00FF66", "ZARA is responding.")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 190)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        for voice in voices:
            if "zira" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.say(text)
        engine.runAndWait()
        engine.stop()

        send_status_to_gui("Listening", "#00FFFF", "Listening securely...")

    except Exception as e:
        print("Speak Error:", e)
        send_status_to_gui("Error", "#FF4444", "Speech error.")

def listen():
    r = sr.Recognizer()

    try:
        try:
            send_status_to_gui("Listening", "#00FFFF", "Listening securely...")
        except:
            pass
        with sr.Microphone() as source:
            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=0.1)

            r.pause_threshold = 0.5
            r.energy_threshold = 300

            audio = r.listen(
                source,
                timeout=2,
                phrase_time_limit=3
            )

        command = r.recognize_google(audio)

        print("You:", command)
        try:
            send_to_gui("You", command)
        except:
            pass

        try:
            send_status_to_gui("Thinking", "#FFAA00", "Processing your command.")
        except:
            pass

        return command.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except Exception as e:
        print("Listen Error:", e)
        return ""

def clean_reply(text):
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    return text.strip()

def greet_user():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak(f"Good morning {USER_NAME}. {ASSISTANT_NAME} is online.")
    elif hour < 18:
        speak(f"Good afternoon {USER_NAME}. {ASSISTANT_NAME} is online.")
    else:
        speak(f"Good evening {USER_NAME}. {ASSISTANT_NAME} is online.")

def is_wakeup_command(command):
    return is_wake_word(command)

def thinking_message():
    messages = [
        "Let me think.",
        "One moment.",
        "Checking that for you.",
        "Let me see.",
        "Sure, give me a second."
    ]
    speak(random.choice(messages))

def change_volume(action):
    if action == "up":
        pyautogui.press("volumeup", presses=5)
        speak("Volume increased.")

    elif action == "down":
        pyautogui.press("volumedown", presses=5)
        speak("Volume decreased.")

    elif action == "mute":
        pyautogui.press("volumemute")
        speak("Volume muted.")

    elif action == "unmute":
        pyautogui.press("volumemute")
        speak("Volume unmuted.")

def get_weather(city="Hyderabad"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return "Sorry, I could not get the weather right now."

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "Sorry, I could not find that on Wikipedia."

def run_zara(command):
    global CONVERSATION_MODE
    
    if command == "":
        return

    if is_wakeup_command(command):
        CONVERSATION_MODE = True

        speak(f"Yes {USER_NAME}, I am ready.")

        try:
            from gui_bridge import show_gui
            show_gui()
        except:
            pass

        return

    elif "close zara" in command or "shutdown zara" in command:
        CONVERSATION_MODE = False

        speak("Going silent.")

        try:
            from gui_bridge import hide_gui
            hide_gui()
        except:
            pass

        return

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")

    elif "who are you" in command:
        speak("I am ZARA, your personal AI assistant.")

    elif "what is your name" in command:
        speak("My name is ZARA.")

    elif "who created you" in command:
        speak("I was created by Sangeeth.")

    elif "volume up" in command or "increase volume" in command:
        change_volume("up")

    elif "volume down" in command or "decrease volume" in command:
        change_volume("down")

    elif "mute volume" in command or command == "mute":
        change_volume("mute")

    elif "unmute volume" in command or command == "unmute":
        change_volume("unmute")

    elif command.startswith("remember my"):
        data = command.replace("remember my", "").strip()

        if " is " in data:
            key, value = data.split(" is ", 1)
            remember(key.strip(), value.strip())
            speak(f"I will remember that your {key.strip()} is {value.strip()}")
        else:
            speak("Please say it like, remember my favorite language is Java.")

    elif command.startswith("what is my"):
        key = command.replace("what is my", "").strip()
        value = recall(key)

        if value:
            speak(f"Your {key} is {value}")
        else:
            speak(f"I don't remember your {key} yet.")

    elif "show all memories" in command or "show my memories" in command:
        memory = load_memory()

        if memory:
            speak("Here are your saved memories.")
            for key, value in memory.items():
                speak(f"Your {key} is {value}")
        else:
            speak("You do not have any saved memories yet.")

    elif "delete memory" in command or "forget my" in command:
        key = command.replace("delete memory", "").replace("forget my", "").strip()
        memory = load_memory()

        if key in memory:
            del memory[key]
            save_memory(memory)
            speak(f"I forgot your {key}.")
        else:
            speak(f"I could not find memory for {key}.")

    elif "clear all memory" in command:
        clear_all_memory()
        speak("All memory has been cleared.")

    elif "search memory" in command:
        keyword = command.replace("search memory", "").strip()

        if keyword:
            results = search_memory(keyword)

            if results:
                speak("I found these memories.")
                for key, value in results.items():
                    speak(f"Your {key} is {value}")
            else:
                speak("No matching memory found.")
        else:
            speak("Please tell me what to search in memory.")

    elif "take note" in command:
        note = command.replace("take note", "").strip()

        if note:
            add_note(note)
            speak("Note saved.")
        else:
            speak("Please tell me the note.")

    elif "show my notes" in command:
        notes = get_notes()

        if notes:
            speak("Here are your notes.")
            for note in notes:
                speak(note)
        else:
            speak("You do not have any notes yet.")

    elif "add task" in command:
        task = command.replace("add task", "").strip()

        if task:
            add_task(task)
            speak("Task added.")
        else:
            speak("Please tell me the task.")

    elif "show my tasks" in command:
        tasks = get_tasks()

        if tasks:
            speak("Here are your tasks.")
            for task in tasks:
                speak(task)
        else:
            speak("You do not have any tasks yet.")

    elif "clear tasks" in command:
        clear_tasks()
        speak("All tasks cleared.")

    elif "add reminder" in command:
        reminder = command.replace("add reminder", "").strip()

        if reminder:
            add_reminder(reminder)
            speak("Reminder saved.")
        else:
            speak("Please tell me the reminder.")

    elif "show reminders" in command:
        reminders = get_reminders()

        if reminders:
            speak("Here are your reminders.")
            for reminder in reminders:
                speak(reminder)
        else:
            speak("You do not have any reminders.")

    elif "clear reminders" in command:
        clear_reminders()
        speak("All reminders cleared.")

    elif "remind me to" in command and " at " in command:
        try:
            task = command.split("remind me to")[1].split(" at ")[0].strip()
            time_text = command.split(" at ")[1].strip().upper()

            add_timed_reminder(task, time_text)

            speak(f"Reminder set for {time_text}")

        except:
            speak("Please say it like: remind me to study java at 08:00 PM")

    elif "show timed reminders" in command:
        reminders = get_timed_reminders()

        if reminders:
            speak("Here are your timed reminders.")

            for reminder in reminders:
                speak(f"{reminder['task']} at {reminder['time']}")
        else:
            speak("No timed reminders found.")

    elif "clear timed reminders" in command:
        clear_timed_reminders()
        speak("All timed reminders cleared.")

    elif "take screenshot" in command or "capture screen" in command:
        screenshot_folder = "screenshots"

        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        file_name = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
        file_path = os.path.join(screenshot_folder, file_name)

        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)

        speak("Screenshot captured and saved.")

    elif "open desktop" in command:
        speak("Opening Desktop")
        os.startfile(os.path.join(os.path.expanduser("~"), "Desktop"))

    elif "open downloads" in command:
        speak("Opening Downloads")
        os.startfile(os.path.join(os.path.expanduser("~"), "Downloads"))

    elif "create folder" in command:
        folder_name = command.replace("create folder", "").strip()

        if folder_name == "":
            speak("Please tell me the folder name.")
        else:
            folder_path = os.path.join(os.path.expanduser("~"), "Desktop", folder_name)
            os.makedirs(folder_path, exist_ok=True)
            speak(f"Folder {folder_name} created on Desktop.")

    elif "create file" in command:
        file_name = command.replace("create file", "").strip()

        if file_name == "":
            speak("Please tell me the file name.")
        else:
            if "." not in file_name:
                file_name += ".txt"

            file_path = os.path.join(os.path.expanduser("~"), "Desktop", file_name)

            with open(file_path, "w") as file:
                file.write("Created by ZARA.")

            speak(f"File {file_name} created on Desktop.")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open vs code" in command or "open vscode" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "close chrome" in command or "close youtube" in command or "close google" in command:
        speak("Closing Chrome")
        os.system("taskkill /f /im chrome.exe")

    elif "close vs code" in command or "close vscode" in command:
        speak("Closing Visual Studio Code")
        os.system("taskkill /f /im Code.exe")

    elif "close calculator" in command:
        speak("Closing Calculator")
        os.system("taskkill /f /im CalculatorApp.exe")

    elif "close notepad" in command:
        speak("Closing Notepad")
        os.system("taskkill /f /im notepad.exe")

    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "search youtube for" in command:
        query = command.replace("search youtube for", "").strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "battery status" in command or "battery percentage" in command:
        battery = psutil.sensors_battery()

        if battery:
            percent = battery.percent
            if battery.power_plugged:
                speak(f"Battery is at {percent} percent and charging.")
            else:
                speak(f"Battery is at {percent} percent.")
        else:
            speak("Battery information is not available.")

    elif "cpu usage" in command:
        cpu = psutil.cpu_percent(interval=1)
        speak(f"CPU usage is {cpu} percent.")

    elif "ram usage" in command or "memory usage" in command:
        ram = psutil.virtual_memory()
        speak(f"RAM usage is {ram.percent} percent.")

    elif "disk usage" in command:
        disk = psutil.disk_usage("C:\\")
        speak(f"Disk usage is {disk.percent} percent.")

    elif "lock computer" in command:
        speak("Locking computer.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif "shutdown computer" in command:
        speak("Shutting down computer in 5 seconds.")
        os.system("shutdown /s /t 5")

    elif "restart computer" in command:
        speak("Restarting computer in 5 seconds.")
        os.system("shutdown /r /t 5")

    elif "cancel shutdown" in command:
        speak("Shutdown cancelled.")
        os.system("shutdown /a")

    elif "exit" in command or "stop" in command:
        speak(f"Goodbye {USER_NAME}.")
        exit()

    elif "weather" in command:
        city = command.replace("weather in", "").replace("weather", "").strip()

        if city == "":
            city = "Hyderabad"

        result = get_weather(city)
        speak(result)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()

        if query:
            result = search_wikipedia(query)
            speak(result[:500])
        else:
            speak("Please tell me what to search on Wikipedia.")

    elif (
        "analyze screen" in command
        or "what is on my screen" in command
        or "what error is on my screen" in command
        or "explain this code" in command
        or "summarize this webpage" in command
        or "what is this application" in command
    ):
        speak("Analyzing your screen.")
        result = analyze_screen(command)
        result = clean_reply(result)
        speak(result[:800])

    elif "summarize pdf" in command or "summarise pdf" in command or "read latest pdf" in command:
        speak("Reading PDF.")
        result = summarize_latest_pdf()
        result = clean_reply(result)
        speak(result[:800])

    elif "show desktop files" in command:
        files = list_files(get_desktop_path())

        if files:
            speak("Here are some desktop files.")
            for file in files:
                speak(file)
        else:
            speak("No files found on Desktop.")

    elif "show downloads files" in command or "show downloaded files" in command:
        files = list_files(get_downloads_path())

        if files:
            speak("Here are some downloads files.")
            for file in files:
                speak(file)
        else:
            speak("No files found in Downloads.")

    elif "find pdf files" in command:
        pdfs = find_pdf_files(get_desktop_path())

        if pdfs:
            speak("I found these PDF files on Desktop.")
            for pdf in pdfs[:5]:
                speak(os.path.basename(pdf))
        else:
            speak("No PDF files found on Desktop.")

    elif "find my" in command:
        keyword = command.replace("find my", "").strip()

        if keyword:
            matches = find_files_by_keyword(get_desktop_path(), keyword)

            if matches:
                speak(f"I found {len(matches)} matching file.")
                speak(os.path.basename(matches[0]))
            else:
                speak(f"I could not find any file matching {keyword}.")
        else:
            speak("Please tell me what file to find.")

    elif "open latest pdf" in command:
        pdfs = find_pdf_files(get_desktop_path())

        if pdfs:
            latest_pdf = max(pdfs, key=os.path.getctime)
            speak("Opening latest PDF.")
            open_file(latest_pdf)
        else:
            speak("No PDF found on Desktop.")

    elif "register face" in command:
        speak("Look at the camera.")
        success, message = register_face()
        speak(message)

    elif "verify face" in command or "face login" in command:
        speak("Verifying your face.")
        success, message = verify_face()

        if success:
            speak("Welcome back Sangeeth.")
        else:
            speak(message)

    elif "fix this error" in command:
        speak("Analyzing error.")
        result = fix_error()
        speak(clean_reply(result)[:800])

    elif "optimize this code" in command:
        speak("Analyzing code.")
        result = optimize_code()
        speak(clean_reply(result)[:800])

    elif "generate test cases" in command:
        speak("Generating test cases.")
        result = generate_test_cases()
        speak(clean_reply(result)[:800])

    elif "explain this program" in command:
        speak("Explaining code.")
        result = explain_code()
        speak(clean_reply(result)[:800])

    else:
        thinking_message()
        try:
            send_status_to_gui("Thinking", "#FFAA00", "Processing your command.")
        except:
            pass

        reply = ask_ai(command)
        reply = clean_reply(reply)
        speak(reply[:500])

def listen_loop():
    global CONVERSATION_MODE
    greet_user()

    while True:

        due_reminders = check_due_reminders()

        for index, task in due_reminders:
            speak(f"Sangeeth, reminder. {task}")
            mark_reminder_done(index)

        command = listen()

        if command:
            if CONVERSATION_MODE:
                run_zara(command)

            elif is_wakeup_command(command):
                run_zara(command)

if __name__ == "__main__":
    listen_loop()