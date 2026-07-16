# ReadingWebApp-with-AI 📖🤖

An AI-powered reading coach web application built with Streamlit, designed to help children (especially 6th graders) improve their reading fluency and pronunciation in real time.

## ✨ Features

- **Real-Time Speech Recognition** — As you read aloud, words turn Green ✅ (correct) or Red ❌ (wrong) instantly using the Web Speech API.
- **AI Reading Coach** — Tracks every word. Detects errors, skips, and correct reads live.
- **Smart Buzzer** 🔔 — Plays an alarm sound immediately when a wrong word is detected.
- **Indian Accent Teacher Voice** 🇮🇳 — If a child mispronounces a word 6+ times in a row, the system automatically speaks the correct word aloud in an Indian English accent, just like a real teacher!
- **Reading Analytics** — Tracks WPM (Words Per Minute), accuracy %, correct words, errors, and skipped words.
- **6th Grade Article Library** — Includes rich articles on Science (Water Cycle, Solar System, Digestive System, Amazon Rainforest) and History (Ancient Rome, Ancient India).
- **Wikipedia Article Import** — Load any Wikipedia article directly into the reading coach.

## 🛠 Tech Stack

- **Frontend:** Streamlit + Vanilla HTML/CSS/JS (custom component)
- **Speech Recognition:** Web Speech API (Chrome/Edge)
- **Text-to-Speech:** Web Speech Synthesis API (Indian accent `en-IN`)
- **Audio Feedback:** Base64-embedded WAV buzzer
- **Backend:** Python 3.10+
- **AI Models:** Whisper (OpenAI), CTranslate2, Torch

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Vishaldubey2210/ReadingWebApp-with-AI.git
cd ReadingWebApp-with-AI
```

### 2. Create a virtual environment
```bash
python -m venv env
env\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

## 📁 Project Structure

```
ReadingWebApp-with-AI/
├── app.py                  # Main Streamlit app
├── ui/
│   └── realtime_reader.py  # Real-time reading coach component
├── articles/
│   └── system/en/
│       ├── medium/science/ # Science articles
│       └── medium/history/ # History articles
├── core/                   # Core logic modules
├── services/               # AI/ML service integrations
├── database/               # Database models
├── requirements.txt
└── README.md
```

## 📜 License

MIT License — free to use, modify, and distribute.

---
Made with ❤️ for young readers 🌟
