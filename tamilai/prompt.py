"""
Tamil LLM Prompt Engineering & Context Formatter
================================================
Provides system prompts, templates, and contextual wrappers optimized
for LLM generation in Tamil.
"""

from typing import Dict, Optional

PROMPT_TEMPLATES = {
    "translate_en_ta": """You are an expert Tamil translator. Translate the following English text into clear, modern, and grammatically accurate Tamil script (தமிழ் எழுத்துக்கள்). Preserve natural phrasing and proper honorifics.

Text:
"{text}"

Tamil Translation:""",

    "translate_tanglish_ta": """You are a Tamil linguistic expert. Convert the following Tanglish (Romanized Tamil) text into formal, standard Tamil script (தமிழ் எழுத்துக்கள்).

Text:
"{text}"

Standard Tamil Script:""",

    "fix_grammar": """You are a Tamil grammar editor. Correct any grammatical errors, spelling mistakes, or awkward phrasing in the following Tamil text while retaining the original meaning.

Tamil Text:
"{text}"

Corrected Tamil Text with Explanations:""",

    "summarize_ta": """You are a concise Tamil content summarizer. Summarize the following document into key bullet points in fluent Tamil (தமிழ்).

Document:
"{text}"

Key Highlights in Tamil:""",

    "creative_content": """You are an acclaimed Tamil author and poet. Generate creative content based on the following topic. Ensure rich Tamil vocabulary, poetic metaphors, and high cultural resonance.

Topic/Prompt:
"{text}"

Creative Tamil Response:""",
}

def build_prompt(template_key: str, text: str, extra_instructions: Optional[str] = None) -> str:
    """Build a structured LLM prompt tailored for Tamil tasks."""
    template = PROMPT_TEMPLATES.get(template_key, PROMPT_TEMPLATES["translate_en_ta"])
    base_prompt = template.format(text=text)

    if extra_instructions:
        base_prompt += f"\n\nAdditional Requirements:\n{extra_instructions}"

    return base_prompt

def get_available_templates() -> Dict[str, str]:
    """Returns all available prompt templates and descriptions."""
    return {
        "translate_en_ta": "English to Tamil Translation",
        "translate_tanglish_ta": "Tanglish to Pure Tamil Script",
        "fix_grammar": "Tamil Grammar & Spelling Corrector",
        "summarize_ta": "Tamil Text Summarizer",
        "creative_content": "Tamil Creative Story/Poem Generator",
    }
