"""
Tamil Transliteration Engine
============================
Converts phonetic Tanglish (Romanized Tamil) into Unicode Tamil Script.
Uses a hybrid rule-based dictionary + phonetic segmentation engine.
"""

import re

# Direct word mappings for high accuracy on common vocabulary
COMMON_DICTIONARY = {
    "vanakkam": "வணக்கம்",
    "nandri": "நன்றி",
    "nanri": "நன்றி",
    "eppadi": "எப்படி",
    "irukkiringal": "இருக்கிறீர்கள்",
    "irukkiraai": "இருக்கிறாய்",
    "irukken": "இருக்கேன்",
    "irukiren": "இருக்கிறேன்",
    "tamil": "தமிழ்",
    "thamil": "தமிழ்",
    "tamizh": "தமிழ்",
    "anbu": "அன்பு",
    "nanban": "நண்பன்",
    "nanba": "நண்பா",
    "nanbaa": "நண்பா",
    "thozhan": "தோழன்",
    "amma": "அம்மா",
    "appa": "அப்பா",
    "anna": "அண்ணா",
    "akka": "அக்கா",
    "thambi": "தம்பி",
    "tangai": "தங்கை",
    "thangai": "தங்கை",
    "veedu": "வீடு",
    "kalai": "காலை",
    "iravu": "இரவு",
    "madhiyam": "மதியம்",
    "nalla": "நல்ல",
    "romba": "ரொம்ப",
    "miga": "மிக",
    "migavum": "மிகவும்",
    "aam": "ஆம்",
    "illai": "இல்லை",
    "sari": "சரி",
    "en": "என்",
    "enudaiya": "என்னுடைய",
    "un": "உன்",
    "unudaiya": "உன்னுடைய",
    "avar": "அவர்",
    "idhu": "இது",
    "adhu": "அது",
    "edhu": "எது",
    "enge": "எங்கே",
    "ange": "அங்கே",
    "eppodhu": "எப்போது",
    "yen": "ஏன்",
    "yaar": "யார்",
    "yaaru": "யாரு",
    "kaalai": "காலை",
    "vanthachu": "வந்தாச்சு",
    "poda": "போடா",
    "podi": "போடி",
    "vaanga": "வாங்கா",
    "ponga": "போங்கா",
    "seri": "சரி",
}

# Vowels (Uyir eluthukkal)
VOWELS = {
    "ai": "ஐ", "au": "ஔ", "aa": "ஆ", "ee": "ஈ", "oo": "ஊ",
    "ei": "ஏ", "ea": "ஏ", "ou": "ஔ",
    "a": "அ", "i": "இ", "u": "உ", "e": "எ", "o": "ஒ",
}

# Consonants (Mei eluthukkal - base without inherent vowel 'a')
# We map consonant + vowel combinations dynamically.
CONSONANT_MAP = [
    ("ksha", "க்ஷ"), ("sh", "ஷ்"), ("s", "ஸ்"), ("h", "ஹ"), ("j", "ஜ்"),
    ("th", "த்"), ("dh", "த்"), ("t", "ட்"), ("d", "ட்"),
    ("ng", "ங்"), ("nj", "ஞ்"), ("ny", "ஞ்"),
    ("zh", "ழ்"), ("l", "ல்"), ("L", "ள்"), ("rl", "ள்"),
    ("r", "ர்"), ("R", "ற்"), ("tr", "ற்"),
    ("n", "ன்"), ("N", "ண்"), ("nh", "ந்"),
    ("p", "ப்"), ("b", "ப்"), ("f", "ப்"),
    ("m", "ம்"), ("y", "ய்"), ("v", "வ்"), ("w", "வ்"),
    ("ch", "ச்"), ("c", "ச்"), ("k", "க்"), ("g", "க்"),
]

# Standard uyirmei vowel signs attached to base consonants
VOWEL_SIGNS = {
    "aa": "ா", "a": "",
    "ee": "ீ", "i": "ி",
    "oo": "ூ", "u": "ு",
    "ee": "ீ", "ei": "ே", "ea": "ே", "e": "ெ",
    "ai": "ை",
    "oo": "ோ", "ou": "ௌ", "o": "ொ",
}

def transliterate_word(word: str) -> str:
    """Transliterate a single word from Tanglish to Tamil."""
    clean_word = word.lower().strip()
    if clean_word in COMMON_DICTIONARY:
        return COMMON_DICTIONARY[clean_word]

    # Rule-based fallback parser
    res = []
    i = 0
    length = len(word)

    while i < length:
        matched = False
        sub = word[i:].lower()

        # Try consonant + vowel match
        for cons_str, cons_char in CONSONANT_MAP:
            if sub.startswith(cons_str):
                c_len = len(cons_str)
                rem = sub[c_len:]
                # Check if followed by vowel
                v_found = False
                for v_str, v_sign in VOWEL_SIGNS.items():
                    if rem.startswith(v_str):
                        # Base consonant character without virama + vowel sign
                        base_char = cons_char[0] # remove pulli 'க்' -> 'க'
                        res.append(base_char + v_sign)
                        i += c_len + len(v_str)
                        v_found = True
                        matched = True
                        break
                if not v_found:
                    # Pure consonant with pulli
                    res.append(cons_char)
                    i += c_len
                    matched = True
                break

        if matched:
            continue

        # Try independent vowel
        for v_str, v_char in VOWELS.items():
            if sub.startswith(v_str):
                res.append(v_char)
                i += len(v_str)
                matched = True
                break

        if not matched:
            res.append(word[i])
            i += 1

    return "".join(res)

def transliterate_text(text: str) -> str:
    """Transliterate an entire text string preserving punctuation and line breaks."""
    def replace_match(match):
        w = match.group(0)
        return transliterate_word(w)

    return re.sub(r'[a-zA-Z]+', replace_match, text)
