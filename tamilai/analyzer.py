"""
Tamil Text & Sentiment Analyzer
===============================
Analyzes text for Tamil character distribution, linguistic register,
and sentiment score using specialized Tamil NLP heuristics.
"""

import re
from typing import Dict, Any

# Sentiment vocabulary for Tamil
POSITIVE_WORDS = {
    "நல்ல", "அருமை", "சிறப்பு", "அன்பு", "மகிழ்ச்சி", "வெற்றி", "அழகு", "நன்றி",
    "வணக்கம்", "சூப்பர்", "வாழ்த்துக்கள்", "நன்மை", "இனிமை", "இன்பம்", "நம்பிக்கை",
    "nalla", "super", "arumai", "sirappu", "anbu", "magizhchi", "vettri", "azhagu", "nandri"
}

NEGATIVE_WORDS = {
    "கெட்ட", "கோபம்", "துன்பம்", "தோல்வி", "வருத்தம்", "பயம்", "கவலை", "சோகம்",
    "வெறுப்பு", "எரிச்சல்", "பாதிப்பு", "ஏமாற்றம்", "ketta", "sopam", "kobam", "thunbam",
    "tholvi", "varuttham", "bayam", "kavalai", "sogam"
}

FORMAL_INDICATORS = {
    "அவர்களே", "செய்கின்றனர்", "என்று", "எனவே", "ஆகையால்", "நன்றி", "மதிப்பிற்குரிய"
}

INFORMAL_INDICATORS = {
    "டா", "டி", "மச்சி", "பாா", "போடா", "போடி", "ப்ரோ", "bro", "machi", "da", "di"
}

def is_tamil_char(char: str) -> bool:
    """Check if character falls within Unicode Tamil block (0B80-0BFF)."""
    code = ord(char)
    return 0x0B80 <= code <= 0x0BFF

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Perform structural and sentiment analysis on the provided text.
    """
    total_chars = len(text)
    if total_chars == 0:
        return {
            "total_characters": 0,
            "total_words": 0,
            "tamil_character_count": 0,
            "tamil_ratio_percent": 0.0,
            "register": "Unknown",
            "sentiment": "Neutral",
            "sentiment_score": 0.0,
        }

    words = re.findall(r'\w+', text.lower())
    tamil_chars = sum(1 for c in text if is_tamil_char(c))
    tamil_ratio = round((tamil_chars / total_chars) * 100, 2)

    # Register detection
    formal_score = sum(1 for w in words if w in FORMAL_INDICATORS)
    informal_score = sum(1 for w in words if w in INFORMAL_INDICATORS)

    if formal_score > informal_score:
        register = "Formal (முறைசார்)"
    elif informal_score > formal_score:
        register = "Informal/Colloquial (வழக்கு பேச்சு)"
    else:
        register = "Standard/Neutral"

    # Sentiment analysis
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS or any(pw in text for pw in POSITIVE_WORDS))
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS or any(nw in text for nw in NEGATIVE_WORDS))

    if pos_count > neg_count:
        sentiment = "Positive (நேர்மறை)"
        score = round(min(1.0, 0.3 + (pos_count * 0.25)), 2)
    elif neg_count > pos_count:
        sentiment = "Negative (எதிர்மறை)"
        score = round(max(-1.0, -0.3 - (neg_count * 0.25)), 2)
    else:
        sentiment = "Neutral (நடுநிலை)"
        score = 0.0

    return {
        "total_characters": total_chars,
        "total_words": len(words),
        "tamil_character_count": tamil_chars,
        "tamil_ratio_percent": tamil_ratio,
        "register": register,
        "sentiment": sentiment,
        "sentiment_score": score,
        "positive_signals": pos_count,
        "negative_signals": neg_count,
    }
