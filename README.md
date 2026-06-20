# 💊 MedSafe AI — Drug Interaction Checker

> **AI-powered medication safety checker built with Python, Flask & OpenAI GPT-4o**

![MedSafe AI](https://img.shields.io/badge/MedSafe-AI%20Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=for-the-badge&logo=flask)

---

## 🚨 The Problem

- **7,000+ deaths** per year in the US from medication errors
- **125,000+ hospitalizations** annually due to adverse drug interactions
- **~30% are preventable** with proper information
- Most patients take **multiple medications** without knowing dangerous combinations

## 💡 The Solution

MedSafe AI lets anyone instantly check if their medications are safe to take together — powered by OpenAI GPT-4o and presented in clear, plain language that anyone can understand.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Interaction Analysis** | AI checks all pairwise + multi-drug combinations |
| 🔴🟡🟢✅ **Severity Ratings** | Critical / Moderate / Mild / Safe classification |
| 💬 **Follow-up Chat** | Ask questions with full conversation context |
| 📄 **Report Download** | JSON report with timestamp and all findings |
| 🏥 **Emergency Guidance** | Tells users when to seek immediate care |
| 📱 **Responsive Design** | Works on mobile, tablet, and desktop |

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <your-repo>
cd medsafe
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 5. Run the App

```bash
python app.py
```

Open **http://localhost:5000** in your browser 🎉

---

## 🗂️ Project Structure

```
medsafe/
├── app.py                  # Flask app & routes
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── utils/
│   ├── ai_engine.py        # OpenAI GPT integration
│   └── helpers.py          # Validation & utilities
├── templates/
│   └── index.html          # Main HTML page
└── static/
    ├── css/style.css       # All styles
    └── js/app.js           # Frontend logic
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main web interface |
| `POST` | `/api/check` | Analyze drug interactions |
| `POST` | `/api/chat` | Follow-up chat with context |
| `POST` | `/api/report` | Generate downloadable report |
| `GET` | `/api/health` | Health check |

### Example: Check Interactions

```bash
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"medicines": ["Warfarin", "Aspirin", "Ibuprofen"]}'
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.0, Flask-CORS |
| **AI Engine** | OpenAI GPT-4o-mini |
| **Frontend** | Vanilla JS, CSS3, Inter font |
| **State Mgmt** | Flask Sessions |
| **Deployment** | Gunicorn (production-ready) |

---

## 🌐 Deploy to Production

### Using Gunicorn (Linux/Mac)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## ⚕️ Disclaimer

MedSafe AI is for **informational purposes only** and does not constitute medical advice. Always consult a licensed healthcare professional before making medication decisions.

---

## 👥 Team

Built for [Hackathon Name] · Healthcare Track · 2024

---

*Making medication safety accessible to everyone.*
