"""
Tamil Text-To-Speech (TTS) Engine Bridge
========================================
Integrates with Termux Android API (`termux-tts-speak`) and Linux `espeak-ng`
to provide offline/online Tamil voice output.
"""

import subprocess
import shutil
from typing import Dict, Any

def detect_tts_engine() -> Dict[str, bool]:
    """Detect available TTS binaries on system."""
    return {
        "termux_tts": shutil.which("termux-tts-speak") is not None,
        "espeak_ng": shutil.which("espeak-ng") is not None,
        "espeak": shutil.which("espeak") is not None,
    }

def speak_tamil(text: str, engine: str = "auto") -> Dict[str, Any]:
    """
    Speak Tamil text using the best available local engine.
    """
    available = detect_tts_engine()

    if engine == "auto":
        if available["termux_tts"]:
            engine = "termux_tts"
        elif available["espeak_ng"]:
            engine = "espeak_ng"
        elif available["espeak"]:
            engine = "espeak"
        else:
            engine = "none"

    if engine == "termux_tts":
        try:
            # Execute termux-tts-speak with language flag
            cmd = ["termux-tts-speak", "-l", "ta", text]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                return {"status": "success", "engine": "termux-tts-speak", "message": "Spoken via Android TTS API"}
            else:
                # Fallback without language flag
                cmd_fallback = ["termux-tts-speak", text]
                subprocess.run(cmd_fallback, capture_output=True, text=True, timeout=10)
                return {"status": "success", "engine": "termux-tts-speak (default language)", "message": "Spoken via Android TTS API"}
        except Exception as e:
            return {"status": "error", "engine": engine, "message": str(e)}

    elif engine in ("espeak_ng", "espeak"):
        binary = "espeak-ng" if available["espeak_ng"] else "espeak"
        try:
            cmd = [binary, "-v", "ta", text]
            subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return {"status": "success", "engine": binary, "message": f"Spoken via {binary} Tamil voice"}
        except Exception as e:
            return {"status": "error", "engine": engine, "message": str(e)}

    return {
        "status": "unavailable",
        "engine": "none",
        "message": "No TTS engine found. Install `termux-api` package in Termux or `espeak-ng` via pkg/apt."
    }
