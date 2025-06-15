import os
import sys
import tkinter as tk
import pyperclip
import threading
import time
from PIL import Image, ImageTk
from tkinter import Toplevel, Button, Text
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
import google.generativeai as genai
from datetime import datetime
import speech_recognition as sr
import socket  # for internet checking

GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)


def is_connected():
    try:
        # Tries to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


# Floating Emoji Assistant
# This code creates a floating emoji assistant that monitors the clipboard for new text.

class FloatingEmojiAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)           # Remove border
        self.root.attributes("-topmost", True)      # Always on top
        self.root.geometry("80x80+1200+600")        # Small icon window (position it bottom-right-ish)
        self.root.config(bg='white')
        self.root.wm_attributes('-transparentcolor', 'white')
        self.is_dragging = False
        self.reminders = []
        threading.Thread(target=self.check_reminders, daemon=True).start()

        
        # Clipboard data tracking
        self.last_clipboard = ""
        self.clipboard_has_new_text = False

        # Emoji Display
        # Get correct path whether running as script or from .exe
        BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        emoji_path = os.path.join(BASE_DIR, "emoji.png")

        # Load emoji icon image
        emoji_image = Image.open(emoji_path).resize((64, 64), Image.Resampling.LANCZOS)
        self.emoji_photo = ImageTk.PhotoImage(emoji_image)

        self.emoji_label = tk.Label(
            self.root,
            image=self.emoji_photo,
            bg="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.emoji_label.pack()

        # Red Dot Indicator (hidden by default)
        self.red_dot = tk.Canvas(self.root, width=12, height=12, bg="white", highlightthickness=0)
        self.red_circle = self.red_dot.create_oval(2, 2, 10, 10, fill="red")
        self.red_dot.place(x=50, y=5)  # Position top-right of emoji
        self.red_dot.place_forget()

        # Event Bindings
        self.root.bind("<ButtonRelease-1>", self.on_click)
        self.emoji_label.bind("<ButtonRelease-1>", self.on_click)


        self.root.bind("<ButtonPress-1>", self.click_mouse)
        self.root.bind("<B1-Motion>", self.drag_window)

        # Start clipboard monitor thread
        threading.Thread(target=self.monitor_clipboard, daemon=True).start()



    def click_mouse(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        self.is_dragging = False  # Reset dragging flag


    def drag_window(self, event):
        self.is_dragging = True  # Mark as dragging

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        win_width = 80
        win_height = 80

        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y

        x = max(0, min(x, screen_width - win_width))
        y = max(0, min(y, screen_height - win_height))

        self.root.geometry(f"+{x}+{y}")


    def monitor_clipboard(self):
        while True:
            try:
                current = pyperclip.paste()
                if current != self.last_clipboard and current.strip() != "":
                    self.last_clipboard = current
                    self.show_red_dot()
            except Exception as e:
                print("Clipboard error:", e)
            time.sleep(1)
    def check_reminders(self):
        while True:
            now = datetime.now().strftime("%H:%M")
            for reminder in self.reminders[:]:  # Copy to avoid issues while removing
                if reminder['time'] == now:
                    messagebox.showinfo("Reminder", f"🔔 Reminder: {reminder['text']}")
                    self.reminders.remove(reminder)
            time.sleep(30)  # Check every 30 seconds

        
    def set_reminder(self):
        reminder_window = Toplevel(self.root)
        reminder_window.title("Set Reminder")
        reminder_window.geometry("300x150")
        reminder_window.attributes("-topmost", True)

        tk.Label(reminder_window, text="Reminder Text:").pack(pady=(10, 0))
        text_entry = tk.Entry(reminder_window, width=30)
        text_entry.pack(pady=(0, 10))

        tk.Label(reminder_window, text="Time (HH:MM 24hr):").pack()
        time_entry = tk.Entry(reminder_window, width=10)
        time_entry.pack(pady=(0, 10))

        def save_reminder():
            text = text_entry.get().strip()
            time_str = time_entry.get().strip()
            try:
                datetime.strptime(time_str, "%H:%M")  # Validate time format
                self.reminders.append({"text": text, "time": time_str})
                messagebox.showinfo("Saved", "Reminder set!")
                reminder_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Time", "Please enter time in HH:MM format.")

        Button(reminder_window, text="Save Reminder", command=save_reminder).pack(pady=5)



    def show_red_dot(self):
        self.red_dot.place(x=50, y=5)

    def hide_red_dot(self):
        self.red_dot.place_forget()

    def on_click(self, event=None):
        if self.is_dragging:
            return  # Don't open dialog if it was a drag
        self.hide_red_dot()
        self.show_dialog()




    def summarize_text(self):

        if not is_connected():
            messagebox.showerror("No Internet", "This feature requires an internet connection.")
            return

        try:
            input_text = self.text_area.get("1.0", tk.END).strip()

            if not input_text:
                messagebox.showwarning("Empty", "Clipboard is empty.")
                return

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Summarize the following:\n\n{input_text}")
            summary = response.text.strip()

            messagebox.showinfo("Summary", summary)
        
        except Exception as e:
            messagebox.showerror("Error", f"Gemini error:\n{str(e)}")


    def translate_text(self):


        if not is_connected():
            messagebox.showerror("No Internet", "This feature requires an internet connection.")
            return
        try:
            input_text = self.text_area.get("1.0", tk.END).strip()

            if not input_text:
                messagebox.showwarning("Empty", "Clipboard is empty.")
                return

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Translate this to Hindi:\n\n{input_text}")
            translation = response.text.strip()

            messagebox.showinfo("Translated", translation)
        
        except Exception as e:
            messagebox.showerror("Error", f"Gemini error:\n{str(e)}")



        
        
        
    def show_dialog(self):
        # Prevent multiple dialogs
        if hasattr(self, 'dialog') and self.dialog.winfo_exists():
            self.dialog.lift()
            return

        # Create new dialog window
        self.dialog = Toplevel(self.root)
        self.dialog.title("Assistant")
        self.dialog.attributes("-topmost", True)
        self.dialog.geometry("400x250")  # Adjust based on your screen size (~1/8th)
        self.dialog.resizable(False, False)

        # Display copied text in a scrollable text area
        self.text_area = ScrolledText(self.dialog, wrap=tk.WORD, height=8)
        self.text_area.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        self.text_area.insert("1.0", self.last_clipboard)
        # Keep it editable now — no need to disable


        # Buttons for summarize and translate
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=(0, 10))

        summarize_btn = Button(button_frame, text="Summarize", command=self.summarize_text)
        translate_btn = Button(button_frame, text="Translate", command=self.translate_text)

        summarize_btn.grid(row=0, column=0, padx=10)
        translate_btn.grid(row=0, column=1, padx=10)

        # Reminder button
        reminder_btn = Button(button_frame, text="Set Reminder", command=self.set_reminder)
        reminder_btn.grid(row=0, column=2, padx=10)

        # Voice to Text Button
        voice_btn = Button(button_frame, text="🎙️ Speak", command=self.voice_to_text)
        voice_btn.grid(row=0, column=3, padx=10)



    def voice_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                messagebox.showinfo("Listening", "Speak now...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", text)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand your speech.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Speech recognition service failed: {e}")
            except Exception as e:
                messagebox.showerror("Error", str(e))



    def run(self):
        self.root.mainloop()
# 
