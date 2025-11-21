# Voice Lab Assistant (Python)

A small voice-driven virtual assistant built in Python using VS Code, designed with an
acoustic test lab workflow in mind (inspired by GRAS Sound & Vibration style tasks).

## Features

- **Voice Interaction**
  - Listens via the default microphone using `SpeechRecognition`.
  - Speaks responses using offline `pyttsx3` text-to-speech.

- **Measurement Sessions**
  - `start session` — creates a timestamped log file in `logs/`.
  - `note ...` or `log ...` — appends time-stamped notes to the current session.
  - `show logs` — prints the most recent session files and their last lines.

- **Simple Audio Measurement**
  - `measure level` — records a short clip from the microphone and computes:
    - RMS value
    - dBFS level (relative to full scale)
  - Gives a qualitative description ("very quiet", "moderate", "loud") and logs the result.

- **Extensible Command System**
  - A tiny rule-based parser (`command_parser.py`) maps natural language into actions.
  - Easy to extend with new commands (e.g., starting external measurement scripts, opening reports, etc.).

## Tech Stack

- Python 3.x
- `SpeechRecognition` + `PyAudio` for microphone STT
- `pyttsx3` for offline TTS
- `sounddevice` + `numpy` for audio capture and RMS computation
- Tested in Visual Studio Code on Windows

## Running the Project

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the assistant:

bash
Copy code
python main.py
Speak commands such as:

start session

note microphone was clipping during sweep

measure level

show logs

exit

All session logs are written to the logs/ folder.

Possible Extensions
Integrate with measurement scripts (e.g., Python tools that control DAQ hardware).

Add spectral analysis (FFT, 1/3-octave bands) to the measure level command.

Connect to an LLM API for more natural conversation or documentation Q&A.

GUI front-end for manual control and visualization of log files and levels.

yaml
Copy code

---

## 5. How to run it in VS Code (step by step)

1. Open folder in VS Code.
2. Open Terminal (make sure it shows `(venv)` after activation).
3. **Run:**

   ```bash
   python main.py
It should print something like:

text
Copy code
[Aurora] Hello, I'm Aurora, your voice lab assistant. Say 'start session' to begin.
[ASSISTANT] Listening...
Speak clearly into your mic:

“start session”

Then “note microphone was noisy at high level”

Then “measure level”

Check the logs/ folder; you should see files like session_20251121_123456.txt with your notes and RMS measurements.
