import os
import speech_recognition as sr
import pyttsx3
from datetime import datetime

from command_parser import parse_command
from audio_utils import record_rms, qualitative_level, timestamp_string

LOGS_DIR = "logs"

class VoiceAssistant:
    def __init__(self, name="Echo"):
        self.name = name
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.current_session_file = None

        # Ensure logs folder exists
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        # Configure TTS voice if you want
        # voices = self.tts_engine.getProperty('voices')
        # self.tts_engine.setProperty('voice', voices[0].id)  # pick a voice

    # ------------- IO: speak & listen -------------

    def speak(self, text: str):
        """
        Speak text out loud and also print it.
        """
        print(f"[{self.name}] {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_once(self, timeout=5, phrase_time_limit=10):
        """
        Listen once from the microphone and return recognized text (or None).
        """
        with sr.Microphone() as source:
            print("[ASSISTANT] Listening...")
            # Optional: adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=timeout,
                                               phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                print("[ASSISTANT] Listening timed out (no speech detected).")
                return None

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"[USER] {text}")
            return text
        except sr.UnknownValueError:
            print("[ASSISTANT] Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"[ASSISTANT] STT request error: {e}")
            return None

    # ------------- Session & logging -------------

    def start_session(self):
        """
        Create a new measurement session log file.
        """
        ts = timestamp_string()
        filename = os.path.join(LOGS_DIR, f"session_{ts}.txt")
        self.current_session_file = filename

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Measurement session started at {datetime.now()}\n")
            f.write("-" * 50 + "\n")

        self.speak(f"Started a new measurement session: {os.path.basename(filename)}")

    def log_note(self, note: str):
        """
        Append a note to the current session or create a generic log.
        """
        if self.current_session_file is None:
            # Create a generic log if no session is active
            ts = timestamp_string()
            self.current_session_file = os.path.join(LOGS_DIR, f"session_{ts}.txt")
            with open(self.current_session_file, "w", encoding="utf-8") as f:
                f.write(f"Measurement session (auto) started at {datetime.now()}\n")
                f.write("-" * 50 + "\n")

        with open(self.current_session_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] NOTE: {note}\n")

        self.speak("Noted.")

    def show_logs(self, max_files=5):
        """
        List recent log files in the logs directory and show last few lines.
        """
        files = [
            f for f in os.listdir(LOGS_DIR)
            if f.startswith("session_") and f.endswith(".txt")
        ]
        if not files:
            self.speak("I don't see any session logs yet.")
            return

        files = sorted(files, reverse=True)[:max_files]
        self.speak("Here are your most recent session logs.")
        for fname in files:
            path = os.path.join(LOGS_DIR, fname)
            print(f"--- {fname} ---")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # Show last 5 lines
                    tail = "".join(lines[-5:])
                    print(tail)
            except Exception as e:
                print(f"Error reading {fname}: {e}")

    # ------------- Audio measurement -------------

    def measure_level(self):
        """
        Record a short clip and estimate its RMS level.
        """
        self.speak("Recording a short sample to estimate the sound level.")
        rms, rms_db = record_rms(duration=2.0, fs=44100)
        level_desc = qualitative_level(rms_db)

        msg = f"The RMS level is approximately {rms_db:.1f} dB relative to full scale. That sounds {level_desc}."
        self.speak(msg)

        # Also log it if we have a session
        if self.current_session_file is not None:
            with open(self.current_session_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] RMS: {rms_db:.2f} dBFS ({level_desc})\n")

    # ------------- Command handling -------------

    def handle_command(self, command: dict):
        action = command.get("action", "none")

        if action == "none":
            return True  # keep running

        if action == "exit":
            self.speak("Shutting down. Goodbye.")
            return False

        if action == "start_session":
            self.start_session()
            return True

        if action == "log_note":
            note = command.get("note", "")
            if note:
                self.log_note(note)
            else:
                self.speak("I didn't catch the note.")
            return True

        if action == "show_logs":
            self.show_logs()
            return True

        if action == "measure_level":
            self.measure_level()
            return True

        if action == "smalltalk":
            text = command.get("raw", "")
            # For now, just repeat politely.
            self.speak(f"You said: {text}")
            return True

        # Unknown action
        self.speak("I'm not sure how to handle that command yet.")
        return True

    # ------------- Main loop -------------

    def run(self):
        """
        Main interaction loop: greet, then repeatedly listen and handle commands.
        """
        self.speak(f"Hello, I'm {self.name}, your voice lab assistant. Say 'start session' to begin.")
        running = True
        while running:
            text = self.listen_once()
            if text is None:
                continue  # try again

            command = parse_command(text)
            running = self.handle_command(command)
