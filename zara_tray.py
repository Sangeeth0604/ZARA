from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import socket
import sys
import os
import subprocess

import zara_background

LOCK_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCK_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    LOCK_SOCKET.bind(("127.0.0.1", 55555))
except OSError:
    print("ZARA is already running.")
    sys.exit()

background_thread = None

def create_icon():
    image = Image.new("RGB", (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill=(0, 255, 255))
    draw.text((24, 18), "Z", fill="black")
    return image

def start_zara():
    global background_thread

    if background_thread is None or not background_thread.is_alive():
        background_thread = threading.Thread(
            target=zara_background.background_loop,
            daemon=True
        )
        background_thread.start()

def open_settings(icon, item):
    subprocess.Popen(["python", "settings_gui.py"])

def quit_app(icon):
    icon.stop()
    os._exit(0)

icon = Icon(
    "ZARA",
    create_icon(),
    menu=Menu(
        MenuItem("Start ZARA", start_zara),
        MenuItem("Settings", open_settings),
        MenuItem("Exit", quit_app)
    )
)

start_zara()
icon.run()