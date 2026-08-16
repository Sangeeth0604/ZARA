import tkinter as tk
from tkinter import scrolledtext
import datetime
import gui_bridge
import json
import os

LOG_FILE = "zara_gui_log.jsonl"
STATUS_FILE = "zara_gui_status.json"

class ZaraWorkingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZARA Active")
        self.root.geometry("480x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#050505")

        self.running = True
        self.dot_count = 0

        self.title = tk.Label(
            self.root,
            text="ZARA ACTIVE",
            font=("Arial", 26, "bold"),
            bg="#050505",
            fg="#00FFFF"
        )
        self.title.pack(pady=15)

        self.brain = tk.Label(
            self.root,
            text="🧠",
            font=("Arial", 66),
            bg="#050505",
            fg="white"
        )
        self.brain.pack(pady=5)

        self.status = tk.Label(
            self.root,
            text="Status: 🟢 Listening",
            font=("Arial", 15, "bold"),
            bg="#050505",
            fg="#00FF66"
        )
        self.status.pack(pady=8)

        self.clock = tk.Label(
            self.root,
            text="Time: --:--",
            font=("Arial", 12),
            bg="#050505",
            fg="#FFFFFF"
        )
        self.clock.pack(pady=4)

        self.face = tk.Label(
            self.root,
            text="Face: ✅ Verified",
            font=("Arial", 12),
            bg="#050505",
            fg="#00FF66"
        )
        self.face.pack(pady=4)

        self.privacy = tk.Label(
            self.root,
            text="Privacy Mode: 🔒 Protected",
            font=("Arial", 12),
            bg="#050505",
            fg="#BBBBBB"
        )
        self.privacy.pack(pady=4)

        self.message = tk.Label(
            self.root,
            text="Listening securely...",
            font=("Arial", 12),
            bg="#050505",
            fg="white"
        )
        self.message.pack(pady=8)

        self.chat_box = scrolledtext.ScrolledText(
            self.root,
            width=54,
            height=12,
            font=("Consolas", 9),
            bg="#111111",
            fg="white",
            insertbackground="white",
            state=tk.DISABLED
        )
        self.chat_box.pack(pady=10)

        self.info = tk.Label(
            self.root,
            text="Say 'close zara' to go silent",
            font=("Arial", 10),
            bg="#050505",
            fg="#888888"
        )
        self.info.pack(pady=5)

        self.close_button = tk.Button(
            self.root,
            text="Close Visual",
            font=("Arial", 11, "bold"),
            bg="#FF4444",
            fg="white",
            command=self.close
        )
        self.close_button.pack(pady=10)

        self.last_log_count = 0

        gui_bridge.chat_callback = self.add_message
        gui_bridge.status_callback = self.set_status

        self.animate()
        self.update_clock()
        self.monitor_logs()
        self.monitor_status()

    def add_message(self, sender, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

        if sender.lower() == "you":
            self.set_status("Listening", "#00FFFF", "User command received.")
        else:
            self.set_status("Responding", "#00FF66", "ZARA is responding.")

    def monitor_logs(self):
        try:
            if os.path.exists(LOG_FILE):

                with open(LOG_FILE, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                if len(lines) != getattr(self, "last_log_count", 0):

                    self.chat_box.config(state=tk.NORMAL)
                    self.chat_box.delete("1.0", tk.END)

                    for line in lines[-50:]:
                        try:
                            data = json.loads(line)

                            sender = data["sender"]
                            message = data["message"]

                            self.chat_box.insert(
                                tk.END,
                                f"{sender}: {message}\n\n"
                            )

                        except:
                            pass

                    self.chat_box.config(state=tk.DISABLED)
                    self.chat_box.see(tk.END)

                    self.last_log_count = len(lines)

        except:
            pass

        self.root.after(1000, self.monitor_logs)

    def monitor_status(self):
        try:
            if os.path.exists(STATUS_FILE):

                with open(STATUS_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)

                status = data.get("status", "Listening")
                color = data.get("color", "#00FF66")
                message = data.get("message", "")

                self.status.config(
                    text=f"Status: {status}",
                    fg=color
                )

                self.message.config(text=message)

        except:
            pass

        self.root.after(500, self.monitor_status)

    def set_status(self, status, color, message):
        self.status.config(text=f"Status: {status}", fg=color)
        self.message.config(text=message)

    def animate(self):
        if self.running:
            dots = "." * self.dot_count
            self.brain.config(text="🧠" + dots)

            self.dot_count += 1
            if self.dot_count > 3:
                self.dot_count = 0

            self.root.after(500, self.animate)

    def update_clock(self):
        if self.running:
            now = datetime.datetime.now().strftime("%I:%M:%S %p")
            self.clock.config(text=f"Time: {now}")
            self.root.after(1000, self.update_clock)

    def close(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ZaraWorkingGUI()
    app.run()