import sounddevice as sd
import numpy as np
from datetime import datetime

def record_rms(duration=2.0, fs=44100):
    """
    Record audio from the default microphone and compute the RMS level.
    duration: seconds
    fs: sample rate (Hz)
    Returns (rms, rms_db)
    """
    print(f"[AUDIO] Recording {duration} seconds at {fs} Hz...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Block until recording is done

    # audio is a 2D array: shape (samples, channels); we just flatten
    audio = audio.flatten()

    # Compute RMS (root-mean-square)
    rms = np.sqrt(np.mean(audio ** 2) + 1e-12)  # avoid sqrt(0)

    # Convert to dB (relative to 1.0 full-scale)
    rms_db = 20 * np.log10(rms)

    return rms, rms_db

def qualitative_level(rms_db, threshold_quiet=-40, threshold_loud=-10):
    """
    Return a simple text description of the level based on thresholds in dBFS.
    """
    if rms_db < threshold_quiet:
        return "very quiet / noise floor"
    elif rms_db < threshold_loud:
        return "moderate level"
    else:
        return "quite loud / close to clipping"

def timestamp_string():
    """
    Return a simple timestamp string suitable for filenames.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")
