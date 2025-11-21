def parse_command(text: str) -> dict:
    """
    Very simple rule-based parser.
    Input: raw text transcript
    Output: dict like {"action": "start_session"} or {"action": "log_note", "note": "..."}
    """
    if not text:
        return {"action": "none"}

    text = text.lower().strip()

    # Exit / stop
    if any(kw in text for kw in ["exit", "quit", "goodbye", "stop assistant"]):
        return {"action": "exit"}

    # Start a new measurement session
    if "start" in text and "session" in text:
        return {"action": "start_session"}

    # Log a note e.g. "note that mic was clipping" or "log note microphone noisy"
    if text.startswith("note ") or text.startswith("log "):
        # Strip the leading keyword
        if text.startswith("note "):
            note = text[len("note "):]
        elif text.startswith("log "):
            note = text[len("log "):]
        else:
            note = text
        return {"action": "log_note", "note": note}

    # Show recent logs
    if "show" in text and "log" in text:
        return {"action": "show_logs"}

    # Measure sound level
    if "measure" in text and ("level" in text or "volume" in text):
        return {"action": "measure_level"}

    # If nothing matched, treat as a general chat (could route to LLM later)
    return {"action": "smalltalk", "raw": text}
