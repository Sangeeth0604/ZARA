import tkinter as tk
from tkinter import messagebox
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

def save_settings():
    config["user_name"] = user_name_entry.get()
    config["assistant_name"] = assistant_name_entry.get()
    config["wake_word"] = wake_word_entry.get()
    config["voice_rate"] = int(voice_rate_entry.get())
    config["voice_enabled"] = voice_enabled_var.get()
    config["face_verification"] = face_verification_var.get()
    config["vision_enabled"] = vision_enabled_var.get()
    config["gui_enabled"] = gui_enabled_var.get()

    save_config(config)

    messagebox.showinfo(
        "Settings Saved",
        "Settings saved successfully. Restart ZARA to apply changes."
    )

config = load_config()

root = tk.Tk()
root.title("ZARA Settings")
root.geometry("430x520")
root.resizable(False, False)
root.configure(bg="#050505")

title = tk.Label(
    root,
    text="ZARA SETTINGS",
    font=("Arial", 24, "bold"),
    bg="#050505",
    fg="#00FFFF"
)
title.pack(pady=20)

def create_label(text):
    return tk.Label(
        root,
        text=text,
        font=("Arial", 11),
        bg="#050505",
        fg="white"
    )

create_label("User Name").pack()
user_name_entry = tk.Entry(root, font=("Arial", 11), width=30)
user_name_entry.insert(0, config.get("user_name", "Sangeeth"))
user_name_entry.pack(pady=5)

create_label("Assistant Name").pack()
assistant_name_entry = tk.Entry(root, font=("Arial", 11), width=30)
assistant_name_entry.insert(0, config.get("assistant_name", "ZARA"))
assistant_name_entry.pack(pady=5)

create_label("Wake Word").pack()
wake_word_entry = tk.Entry(root, font=("Arial", 11), width=30)
wake_word_entry.insert(0, config.get("wake_word", "wake up zara"))
wake_word_entry.pack(pady=5)

create_label("Voice Rate").pack()
voice_rate_entry = tk.Entry(root, font=("Arial", 11), width=30)
voice_rate_entry.insert(0, str(config.get("voice_rate", 190)))
voice_rate_entry.pack(pady=5)

voice_enabled_var = tk.BooleanVar(value=config.get("voice_enabled", True))
tk.Checkbutton(
    root,
    text="Voice Enabled",
    variable=voice_enabled_var,
    bg="#050505",
    fg="white",
    selectcolor="#111111",
    font=("Arial", 10)
).pack(pady=5)

face_verification_var = tk.BooleanVar(value=config.get("face_verification", True))
tk.Checkbutton(
    root,
    text="Face Verification Enabled",
    variable=face_verification_var,
    bg="#050505",
    fg="white",
    selectcolor="#111111",
    font=("Arial", 10)
).pack(pady=5)

vision_enabled_var = tk.BooleanVar(value=config.get("vision_enabled", True))
tk.Checkbutton(
    root,
    text="Vision AI Enabled",
    variable=vision_enabled_var,
    bg="#050505",
    fg="white",
    selectcolor="#111111",
    font=("Arial", 10)
).pack(pady=5)

gui_enabled_var = tk.BooleanVar(value=config.get("gui_enabled", True))
tk.Checkbutton(
    root,
    text="GUI Enabled",
    variable=gui_enabled_var,
    bg="#050505",
    fg="white",
    selectcolor="#111111",
    font=("Arial", 10)
).pack(pady=5)

save_button = tk.Button(
    root,
    text="Save Settings",
    font=("Arial", 12, "bold"),
    bg="#00FFFF",
    fg="black",
    width=18,
    command=save_settings
)
save_button.pack(pady=20)

footer = tk.Label(
    root,
    text="Privacy-first configuration for ZARA",
    font=("Arial", 9),
    bg="#050505",
    fg="#888888"
)
footer.pack(pady=5)

root.mainloop()