import tkinter as tk
from tkinter import scrolledtext
import threading
import main
import gui_bridge

zara_started = False

def add_message(sender, message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"{sender}: {message}\n\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

def start_zara():
    global zara_started

    if zara_started:
        add_message("ZARA", "I am already running.")
        return

    zara_started = True
    status_label.config(text="Status: Listening...")
    add_message("ZARA", "Assistant started.")

    start_button.config(state=tk.DISABLED)

    threading.Thread(target=main.listen_loop, daemon=True).start()

def stop_zara():
    status_label.config(text="Status: Stopped")
    add_message("ZARA", "Assistant stopped. Close the window to fully exit.")

root = tk.Tk()
root.title("ZARA AI Assistant")
root.geometry("520x620")
root.resizable(False, False)
root.configure(bg="#111111")

title = tk.Label(
    root,
    text="ZARA",
    font=("Arial", 34, "bold"),
    bg="#111111",
    fg="#00FFFF"
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="Your Personal AI Desktop Assistant",
    font=("Arial", 13),
    bg="#111111",
    fg="white"
)
subtitle.pack(pady=5)

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Arial", 12),
    bg="#111111",
    fg="#00FF66"
)
status_label.pack(pady=5)

chat_box = scrolledtext.ScrolledText(
    root,
    width=58,
    height=18,
    font=("Consolas", 10),
    bg="#1E1E1E",
    fg="white",
    insertbackground="white",
    state=tk.DISABLED
)
chat_box.pack(pady=10)

gui_bridge.chat_callback = add_message

button_frame = tk.Frame(root, bg="#111111")
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="Start ZARA",
    font=("Arial", 12, "bold"),
    width=14,
    bg="#00FFFF",
    fg="black",
    command=start_zara
)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(
    button_frame,
    text="Stop",
    font=("Arial", 12, "bold"),
    width=14,
    bg="#FF4444",
    fg="white",
    command=stop_zara
)
stop_button.grid(row=0, column=1, padx=10)

footer = tk.Label(
    root,
    text="Privacy-first AI Assistant by Sangeeth",
    font=("Arial", 9),
    bg="#111111",
    fg="#888888"
)
footer.pack(pady=5)

root.mainloop()