import customtkinter as ctk
from tkinter import END
import speech_recognition as sr
import pyttsx3
import threading
import webbrowser
import requests
from google import genai
import musiclibrary
from datetime import datetime
import time

# ---------------- SETTINGS ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- API KEYS ----------------
newsapi = "23b103d6d530432b85c21b93089187b3"

client = genai.Client(
    api_key="AIzaSyD5VAHrYh-ocZ2UAGICYgGUwbxbbogbnlQ"
)

# ---------------- WINDOW ----------------
app = ctk.CTk()
app.geometry("1200x700")
app.title("JARVIS AI")
app.configure(fg_color="#050816")

# ---------------- VOICE ----------------
def speak(text):


    engine = pyttsx3.init()
    engine.setProperty("rate", 180)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    recognizer = sr.Recognizer()
    running = False


# ---------------- SPEAK ----------------
def speak(text):
    update_status("🗣 Speaking")

    engine.say(text[:300])
    engine.runAndWait()

    update_status("💤 Waiting...")


# ---------------- AI ----------------
def aiprocess(command):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are Jarvis AI assistant.

        User: {command}
        """
    )

    return response.text


# ---------------- STATUS ----------------
def update_status(text):
    status_label.configure(text=text)


# ---------------- TIME ----------------
def update_time():
    while True:
        current = datetime.now().strftime("%I:%M:%S %p")
        date_now = datetime.now().strftime("%d %B %Y")

        time_label.configure(text=current)
        date_label.configure(text=date_now)

        time.sleep(1)


# ---------------- PROCESS COMMAND ----------------
def processcommand(c):
    textbox.insert(END, f"\n🧑 You: {c}\n")

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("Opening Linkedin")

    elif "open crex" in c.lower():
        webbrowser.open("https://crex.com")
        speak("Opening Crex")

    elif c.lower().startswith("play"):
        try:
            song = c.lower().replace("play", "").strip()
            link = musiclibrary.music[song]

            webbrowser.open(link)
            speak(f"Playing {song}")

        except:
            speak("Song not found")

    elif "news" in c.lower():

        update_status("📰 Getting News")

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            for article in articles[:5]:
                headline = article["title"]

                textbox.insert(END, f"📰 {headline}\n")
                speak(headline)

    else:
        update_status("🧠 Thinking")

        output = aiprocess(c)

        textbox.insert(END, f"🤖 Jarvis: {output}\n\n")

        speak(output)


# ---------------- JARVIS LOOP ----------------
def jarvis_loop():
    global running

    speak("Initializing Jarvis")

    while running:
        try:
            with sr.Microphone() as source:
                update_status("🎤 Listening for Jarvis")

                recognizer.adjust_for_ambient_noise(source)

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":

                speak("Yes Sir")

                with sr.Microphone() as source:
                    update_status("⚡ Jarvis Active")

                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=5
                    )

                    command = recognizer.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print(e)


# ---------------- BUTTONS ----------------
def start_jarvis():
    global running

    if not running:
        running = True

        thread = threading.Thread(target=jarvis_loop)
        thread.daemon = True
        thread.start()


def stop_jarvis():
    global running
    running = False
    update_status("⛔ Stopped")


# ---------------- UI ----------------
title = ctk.CTkLabel(
    app,
    text="J.A.R.V.I.S",
    font=("Orbitron", 42, "bold"),
    text_color="#00F5FF"
)
title.pack(pady=15)

time_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 32, "bold"),
    text_color="cyan"
)
time_label.pack()

date_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 18),
    text_color="white"
)
date_label.pack(pady=5)

status_label = ctk.CTkLabel(
    app,
    text="💤 Waiting...",
    font=("Arial", 22),
    text_color="#00ffcc"
)
status_label.pack(pady=10)

textbox = ctk.CTkTextbox(
    app,
    width=1000,
    height=350,
    font=("Consolas", 16),
    corner_radius=20
)
textbox.pack(pady=20)

frame = ctk.CTkFrame(app, fg_color="transparent")
frame.pack()

start_btn = ctk.CTkButton(
    frame,
    text="▶ Start Jarvis",
    command=start_jarvis,
    width=200,
    height=50,
    font=("Arial", 18)
)
start_btn.grid(row=0, column=0, padx=15)

stop_btn = ctk.CTkButton(
    frame,
    text="⛔ Stop",
    command=stop_jarvis,
    width=200,
    height=50,
    font=("Arial", 18)
)
stop_btn.grid(row=0, column=1, padx=15)

exit_btn = ctk.CTkButton(
    frame,
    text="❌ Exit",
    command=app.destroy,
    width=200,
    height=50,
    font=("Arial", 18),
)
exit_btn.grid(row=0, column=2, padx=15)

# ---------------- THREAD ----------------
threading.Thread(target=update_time, daemon=True).start()

app.mainloop()