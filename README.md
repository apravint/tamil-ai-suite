# 🌺 Tamil AI Suite (`tamil-ai-suite`)

> **Open-Source Tamil NLP, Transliteration, Sentiment Analysis & Voice TTS Toolkit for Termux & Linux**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-orange.svg)]()

`tamil-ai-suite` is a high-performance Python toolkit and CLI designed for Tamil text processing, phonetic Tanglish-to-Tamil script transliteration, linguistic sentiment analysis, prompt engineering pipelines, and local offline Text-To-Speech (TTS) voice bridges.

---

## ✨ Features

- ✍️ **Phonetic Tanglish Transliteration**: Convert Romanized Tamil (`vanakkam nanba`) directly into pure Unicode Tamil script (`வணக்கம் நண்பா`).
- 📊 **Linguistic & Sentiment Analyzer**: Measures Tamil character density, formal vs. colloquial register, and emotional sentiment polarity.
- 🤖 **Structured Tamil LLM Prompts**: Ready-to-use prompt templates optimized for English-to-Tamil translation, grammar correction, and creative storytelling.
- 🔊 **Offline TTS Bridge**: Integrates with Android `termux-tts-speak` and Linux `espeak-ng` to speak Tamil text natively.
- 💻 **Interactive Rich Terminal UI**: Interactive command deck for effortless terminal interaction.

---

## 🚀 Quick Start

### Installation

```bash
cd tamil-ai-suite
pip install -e .
```

---

## 🛠️ Usage

### 1. Transliterate Tanglish to Tamil Script
```bash
tamilai transliterate "vanakkam nanba eppadi irukkiraai"
```
**Output:**
```text
Tanglish: vanakkam nanba eppadi irukkiraai
Tamil:    வணக்கம் நண்பா எப்படி இருக்கிறாய்
```

### 2. Analyze Text & Sentiment
```bash
tamilai analyze "தமிழ் மொழி மிகவும் பழமையான மற்றும் அருமையான மொழி!"
```

### 3. Build & Execute Tamil LLM Prompt
```bash
tamilai prompt --type translate_en_ta "Welcome to our AI OS platform"
```

### 4. Speak Tamil via Voice Engine
```bash
tamilai speak "வணக்கம், உங்களை வரவேற்பதில் மகிழ்ச்சி"
```

### 5. Launch Interactive TUI Mode
```bash
tamilai interactive
# or simply run:
tamilai
```

---

## 🌲 Repository Structure

```text
tamil-ai-suite/
├── tamilai/
│   ├── __init__.py
│   ├── cli.py             # CLI runner & Rich TUI dashboard
│   ├── transliterate.py   # Phonetic Tanglish parser engine
│   ├── analyzer.py        # Tamil script & sentiment analyzer
│   ├── prompt.py          # Structured Tamil LLM prompt builder
│   ├── tts.py             # Offline Android/Linux TTS bridge
│   └── llm.py             # Multi-provider LLM connector
├── requirements.txt
├── setup.py
└── README.md
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

Built with ❤️ by **Pravin Tamilan ([@apravint](https://github.com/apravint))**.
