import tkinter as tk
from tkinter import ttk
import threading
import time
import os
from datetime import datetime
import pyautogui

# Session folder setup
BASE_DIR = "logs"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SESSION_DIR = os.path.join(BASE_DIR, f"session_{timestamp}")
SCREENSHOT_DIR = os.path.join(SESSION_DIR, "screenshots")

os.makedirs(SCREENSHOT_DIR)
KEYLOG_FILE = os.path.join(SESSION_DIR, "keystrokes.log")

recording = False


# Keystroke logger (APP LEVEL)
def log_key(event):
    if recording:
        with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {event.char}\n")


# Screenshot capture thread
def capture_screens():
    while recording:
        ts = datetime.now().strftime("%H-%M-%S")
        img_path = os.path.join(SCREENSHOT_DIR, f"screen_{ts}.png")
        pyautogui.screenshot(img_path)
        time.sleep(5)


# Controls
def start_monitoring():
    global recording
    recording = True
    status_label.config(text="● Monitoring ON", foreground="#2ecc71")
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")

    t = threading.Thread(target=capture_screens, daemon=True)
    t.start()


def stop_monitoring():
    global recording
    recording = False
    status_label.config(text="● Monitoring OFF", foreground="#e74c3c")
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")


# UI Setup
root = tk.Tk()
root.title("Consent-Based Activity Monitor")
root.geometry("600x420")
root.configure(bg="#0f172a")  # dark background

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Card.TFrame",
    background="#020617",
    borderwidth=1,
    relief="solid"
)

style.configure(
    "Title.TLabel",
    background="#020617",
    foreground="#38bdf8",
    font=("Segoe UI", 16, "bold")
)

style.configure(
    "Text.TLabel",
    background="#020617",
    foreground="#e5e7eb",
    font=("Segoe UI", 10)
)

style.configure(
    "Status.TLabel",
    background="#020617",
    foreground="#e74c3c",
    font=("Segoe UI", 10, "bold")
)

# Card container
card = ttk.Frame(root, style="Card.TFrame", padding=20)
card.place(relx=0.5, rely=0.5, anchor="center")

# Title
ttk.Label(
    card,
    text="Activity Monitoring Tool",
    style="Title.TLabel"
).pack(pady=(0, 10))

# Subtitle
ttk.Label(
    card,
    text="Consent-based keystroke & screen monitoring (lab use only)",
    style="Text.TLabel"
).pack(pady=(0, 15))

# Text box
text_box = tk.Text(
    card,
    height=6,
    width=55,
    bg="#020617",
    fg="#e5e7eb",
    insertbackground="white",
    relief="solid",
    bd=1
)
text_box.pack(pady=10)
text_box.bind("<Key>", log_key)

# Buttons
btn_frame = ttk.Frame(card, style="Card.TFrame")
btn_frame.pack(pady=15)

start_btn = ttk.Button(btn_frame, text="▶ Start Monitoring", command=start_monitoring)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ttk.Button(btn_frame, text="■ Stop Monitoring", command=stop_monitoring)
stop_btn.grid(row=0, column=1, padx=10)
stop_btn.config(state="disabled")

# Status
status_label = ttk.Label(
    card,
    text="● Monitoring OFF",
    style="Status.TLabel"
)
status_label.pack(pady=(10, 0))

root.mainloop()
