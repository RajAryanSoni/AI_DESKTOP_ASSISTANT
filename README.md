# 🧠 AI_DESKTOP_ASSISTANT (Powered by Google Generative AI)

This is a lightweight desktop AI assistant built using Python that helps you stay productive with quick access to translation and summarization. It appears as a smiley emoji on your screen. When you copy any text, a red dot appears on the emoji. Clicking the emoji reveals a dialog where you can:

- ✨ Summarize copied text
- 🌍 Translate copied text
- 🎤 Speak instead of typing
- 📝 Type and get responses even without copying

“Yes, I could’ve used Google Translate or ChatGPT, but why switch tabs again and again when my assistant floats right on my desktop? Also… I built it, so I love it.”

---

## 🔧 Features

- 📋 Clipboard Monitoring: Detects copied content
- 😃 Emoji Icon Assistant: Stays on your desktop as a friendly smiley
- 🟥 Red Dot Notification: Appears when something is copied
- 💬 Summarize or Translate any text
- 🎙️ Voice-to-text support (Speak instead of typing!)
- 🧠 Powered by Google Generative AI (Gemini)
- 🚫 Graceful fallback for no internet access
- 🧪 Always evolving: UI and functionality will keep improving!

---

## 💻 Technologies Used

- Python `tkinter` (GUI)
- `pyperclip` for clipboard access
- `Pillow` for image handling
- `google-generativeai` for AI response
- `speechrecognition` for voice input

---

## 🚀 Getting Started

### 1. Clone the repo

```bashd
git clone https://github.com/yourusername/desktop-ai-assistant.git
cd desktop-ai-assistant
```
2. Install dependencies
```bashd
   pip install -r requirements.txt
```
3. Run the app
```bashd
  python main.py
```

🗂 Packaging to .exe
If you want the assistant to auto-start with your PC:

```bashd
  pyinstaller --noconfirm --onefile --windowed --add-data "emoji.png;." main.py
```
Then, add the generated main.exe to your Windows startup folder.


📌 Note
Yes, the UI might look a little classic/retro right now. But stay tuned—I’ll keep updating the visuals and functionality in the future!

Feedback is welcome! 💬

🧑‍💻 Author
Made with Creativity⚡ by Raj Aryan.
