# 🎓 Language Agnostic AI Chatbot

> **Smart India Hackathon 2025** · Problem Statement ID: 25104 · Theme: Smart Education

A multilingual education FAQ chatbot that detects the user's language, translates to English, classifies intent using Rasa NLU, retrieves the answer from a 50+ question knowledge base, and translates the response back — all in under 2 seconds.

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Tech Stack](#3-tech-stack)
4. [Architecture](#4-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Installation](#6-installation)
7. [Running the Backend](#7-running-the-backend)
8. [Running the Frontend](#8-running-the-frontend)
9. [Running Rasa](#9-running-rasa)
10. [Sample Screenshots](#10-sample-screenshots)
11. [API Flow](#11-api-flow)
12. [Language Processing Flow](#12-language-processing-flow)
13. [Database Schema](#13-database-schema)
14. [Future Improvements](#14-future-improvements)
15. [License](#15-license)

---

## 1. Project Overview

This project is an **end-to-end multilingual chatbot** designed for Indian educational institutions. Students can type questions in any supported language — Hindi, Tamil, Telugu, Malayalam, English, etc. — and receive accurate answers about admissions, fees, hostel, exams, scholarships, and more.

**Why language agnostic?** Indian students often feel more comfortable asking questions in their native language. This chatbot removes the language barrier from accessing institutional FAQs.

**Problem Statement 25104** from Smart India Hackathon 2025 asked teams to build AI-powered tools for Smart Education. This chatbot addresses multilingual accessibility in educational information systems.

---

## 2. Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **User Query Input** | Clean chat interface with sample question buttons |
| 2 | **Language Detection** | Automatic detection using `langdetect` |
| 3 | **IndicTrans Routing** | Hindi queries routed through IndicTrans pipeline |
| 4 | **Google Translate Routing** | Other Indian languages use Google Translate API |
| 5 | **English Translation** | All queries normalized to English before NLU |
| 6 | **Rasa NLU** | Intent classification on English text |
| 7 | **Slot Filling** | Entity extraction (subject, semester, etc.) |
| 8 | **FAQ Retrieval** | 55 Q&A pairs across 12 categories |
| 9 | **Response Translation** | Answer translated back to user's language |
| 10 | **Chat Interface** | Responsive React UI with pipeline metadata display |

**Logged to SQLite:** Every interaction stores original query, detected language, English query, intent, confidence, response, and timestamp.

---

## 3. Tech Stack

### Backend
| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Primary language |
| **Django 4.2** | Web framework + middleware |
| **Django REST Framework** | JSON API endpoints |
| **SQLite** | Lightweight database via Django ORM |
| **langdetect** | Language detection |
| **deep-translator** | Google Translate + IndicTrans routing |
| **Rasa 3.x** | NLU intent classification + slot filling |

### Frontend
| Tool | Purpose |
|------|---------|
| **React 19** | UI library |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS 3** | Utility-first styling |
| **Vite** | Build tool (fast dev server) |
| **Axios** | HTTP client for API calls |

---

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │           React + TypeScript + Tailwind CSS              │  │
│   │                  (localhost:3000)                        │  │
│   └──────────────────────┬───────────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           │ POST /api/chat/
                           │ { "message": "hostel fees kya hai?" }
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DJANGO BACKEND                              │
│                    (localhost:8000)                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  LanguageMiddleware                       │  │
│  │            (intercepts every /api/chat/ request)          │  │
│  │            → detects language using langdetect            │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    ChatView (views.py)                    │  │
│  │                                                           │  │
│  │   Step 2: Language detected (e.g. 'hi' = Hindi)          │  │
│  │   Step 3: Hindi? → IndicTrans pipeline                   │  │
│  │   Step 4: Others? → Google Translate API                 │  │
│  │   Step 5: English text = "what are hostel fees?"         │  │
│  │   Step 6: Call Rasa NLU server                           │  │
│  │   Step 7: Intent = ask_hostel_fees, confidence = 0.95    │  │
│  │   Step 8: FAQ lookup → "Hostel fees are ₹40,000/year"   │  │
│  │   Step 9: Translate answer back to Hindi                 │  │
│  │   Step 10: Log to SQLite via Django ORM                  │  │
│  └───────────┬───────────────────────┬───────────────────────┘  │
│              │                       │                          │
│              ▼                       ▼                          │
│  ┌──────────────────┐   ┌──────────────────────────────────┐   │
│  │  Rasa NLU Server │   │   SQLite Database (db.sqlite3)   │   │
│  │  (localhost:5005) │   │   Django ORM → ChatLog model     │   │
│  │                  │   │                                  │   │
│  │  /model/parse    │   │  original_query | detected_lang  │   │
│  │  → intent        │   │  english_query  | intent         │   │
│  │  → entities      │   │  response       | timestamp      │   │
│  └──────────────────┘   └──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Fallback behavior:** If Rasa server is not running, a keyword-based classifier is used automatically — the demo works without Rasa.

---

## 5. Folder Structure

```
language-agnostic-chatbot/
│
├── backend/                          # Django backend
│   ├── manage.py                     # Django entry point
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Sample environment variables
│   ├── db.sqlite3                    # SQLite DB (created by `migrate`, git-ignored)
│   │
│   ├── language_agnostic_chatbot/    # Django project config
│   │   ├── settings.py               # All settings (DB, CORS, middleware)
│   │   ├── urls.py                   # Root URL router
│   │   └── wsgi.py
│   │
│   └── chatbot/                      # Main Django app
│       ├── models.py                 # ChatLog model (SQLite schema)
│       ├── views.py                  # ChatView — 10-step pipeline
│       ├── urls.py                   # /api/chat/ and /api/history/
│       ├── translation_service.py    # LangDetect + IndicTrans + Google Translate
│       ├── rasa_client.py            # Rasa NLU client + keyword fallback
│       ├── faq_knowledge_base.py     # 55 Q&A pairs + get_answer()
│       ├── apps.py
│       ├── middleware/
│       │   └── language_middleware.py  # Django middleware
│       └── migrations/
│           └── 0001_initial.py
│
├── frontend/                         # React + TypeScript + Tailwind
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── index.html
│   ├── .env.example
│   │
│   └── src/
│       ├── App.tsx                   # Root component
│       ├── main.tsx                  # React entry point
│       ├── index.css                 # Tailwind directives
│       │
│       ├── components/
│       │   ├── ChatHeader.tsx        # Top bar with title
│       │   ├── ChatWindow.tsx        # Scrollable message list
│       │   ├── ChatInput.tsx         # Input box + send button
│       │   ├── MessageBubble.tsx     # Individual message with metadata
│       │   └── LoadingSpinner.tsx    # Animated dots
│       │
│       ├── hooks/
│       │   └── useChat.ts            # Chat state management hook
│       │
│       ├── types/
│       │   └── index.ts              # TypeScript interfaces
│       │
│       └── utils/
│           └── api.ts                # Axios API calls
│
├── rasa_bot/                         # Rasa NLU configuration
│   ├── config.yml                    # NLU pipeline config
│   ├── domain.yml                    # Intents, entities, slots
│   ├── credentials.yml
│   ├── endpoints.yml
│   └── data/
│       ├── nlu.yml                   # 55 intents × multiple examples
│       ├── stories.yml
│       └── rules.yml
│
├── dataset/
│   └── faq_dataset.csv               # 55 Q&A pairs as CSV
│
├── docs/
│   ├── generate_pdf.py               # Regenerates the PDF (needs reportlab)
│   └── project_documentation.pdf     # 5-page project PDF
│
├── LICENSE
└── README.md
```

---

## 6. Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm 9 or higher

### Step 1 — Clone the repository

```bash
git clone https://github.com/<your-username>/language-agnostic-chatbot.git
cd language-agnostic-chatbot
```

### Step 2 — Set up the Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### Step 3 — Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4 — Install frontend dependencies

```bash
cd ../frontend
npm install
```

### Step 5 — Set up environment variables

```bash
# Backend
cd ../backend
cp .env.example .env

# Frontend
cd ../frontend
cp .env.example .env
```

---

## 7. Running the Backend

```bash
cd backend

# Create the SQLite database tables
python manage.py migrate

# Start the Django development server on port 8000
python manage.py runserver
```

The backend will be available at: **http://localhost:8000**

**Test the API is working:**
```bash
curl http://localhost:8000/api/chat/
# Expected: {"status": "ok", "message": "Language Agnostic AI Chatbot — SIH 2025", ...}
```

**Send a test message:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the hostel fees?"}'
```

---

## 8. Running the Frontend

```bash
cd frontend
npm run dev
```

The React app will open at: **http://localhost:3000**

---

## 9. Running Rasa

Rasa is optional — the backend has a keyword fallback classifier that works without it. To use the full Rasa NLU pipeline:

```bash
# Install Rasa (one-time setup — takes a few minutes)
pip install rasa

# Navigate to rasa directory
cd rasa_bot

# Train the model (first time — takes 2-3 minutes)
rasa train

# Start the Rasa server on port 5005
rasa run --enable-api
```

Once Rasa is running, the backend will automatically use it instead of the keyword classifier.

**Verify Rasa is working:**
```bash
curl -X POST http://localhost:5005/model/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "what are the hostel fees?"}'
```

---

## 10. Sample Screenshots

```
┌───────────────────────────────────────────────────┐
│  🤖 Language Agnostic AI Chatbot     SIH 2025     │
│  ── Language → Translate → Rasa → FAQ → Reply ──  │
├───────────────────────────────────────────────────┤
│                                                   │
│  🎓 Welcome! I am the SIH Education Chatbot...    │
│                                                   │
│                    What are the hostel fees? [U]  │
│                                                   │
│  [AI] Hostel fees are ₹40,000 per year...         │
│       ▼ Show pipeline details                     │
│       🌐 Language: English (en)                   │
│       🔄 Translated via: No translation           │
│       🎯 Intent: ask_hostel_fees (85%)            │
│       ⚡ Time: 124ms                              │
│                                                   │
│        हॉस्टल की फीस कितनी है? [U]               │
│                                                   │
│  [AI] छात्रावास की फीस ₹40,000 प्रति वर्ष है...  │
│       ▼ Show pipeline details                     │
│       🌐 Language: Hindi (hi)                     │
│       🔄 Translated via: IndicTrans (Hindi)       │
│       📝 In English: "what are the hostel fees"   │
│       🎯 Intent: ask_hostel_fees (85%)            │
│       ⚡ Time: 891ms                              │
│                                                   │
├───────────────────────────────────────────────────┤
│  Try: [Hostel fees?] [Exams?] [हिंदी में] ...    │
│  ┌──────────────────────────────────┐  [→ Send]  │
│  │ Ask in any language...           │             │
│  └──────────────────────────────────┘             │
└───────────────────────────────────────────────────┘
```

---

## 11. API Flow

### POST /api/chat/

**Request:**
```json
{
  "message": "छात्रवृत्ति के लिए कैसे आवेदन करें?"
}
```

**Response:**
```json
{
  "response": "छात्रवृत्ति के लिए कॉलेज पोर्टल के 'Scholarships' अनुभाग से आवेदन करें...",
  "detected_language": "Hindi",
  "language_code": "hi",
  "intent": "ask_scholarship_apply",
  "confidence": 0.85,
  "entities": [],
  "english_query": "How to apply for scholarship?",
  "translation_method": "indicTrans",
  "processing_time_ms": 743
}
```

### GET /api/chat/

Health check — returns server status.

### GET /api/history/

Returns last 20 logged interactions from SQLite.

---

## 12. Language Processing Flow

```
User Input (any language)
        │
        ▼
┌───────────────────┐
│  langdetect       │  Detects: 'hi' (Hindi), 'ta' (Tamil), 'en' (English)...
│  Language ID      │
└────────┬──────────┘
         │
         ├─── Hindi ('hi')? ──────────► IndicTrans Pipeline (Hindi → English)
         │
         ├─── Other Indian language? ──► Google Translate API (Lang → English)
         │
         └─── Already English? ────────► No translation needed
                   │
                   ▼
         ┌─────────────────────┐
         │  English Query      │  e.g. "What are the hostel fees?"
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Rasa NLU Server    │  POST /model/parse
         │  or Keyword Fallback│  → intent: "ask_hostel_fees"
         └──────────┬──────────┘  → confidence: 0.95
                    │
                    ▼
         ┌─────────────────────┐
         │  FAQ Knowledge Base │  get_answer("ask_hostel_fees")
         │  (55 Q&A entries)   │  → "Hostel fees are ₹40,000..."
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Translate Back     │  English → User's language
         │  (same routing)     │  IndicTrans for Hindi, Google for others
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Log to SQLite      │  Django ORM → ChatLog model
         └──────────┬──────────┘
                    │
                    ▼
              JSON Response
              → React Frontend
```

---

## 13. Database Schema

**Table: `chatbot_chatlog`** (SQLite via Django ORM)

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Auto-increment primary key |
| `original_query` | TEXT | Raw text typed by the user |
| `detected_language` | VARCHAR(10) | ISO 639-1 code (e.g. 'hi', 'en') |
| `language_name` | VARCHAR(50) | Human-readable name (e.g. 'Hindi') |
| `english_query` | TEXT | Translated English text sent to Rasa |
| `intent` | VARCHAR(100) | Rasa-predicted intent (e.g. 'ask_fees') |
| `intent_confidence` | FLOAT | Rasa confidence score (0.0 – 1.0) |
| `response` | TEXT | Final response sent to user |
| `translation_method` | VARCHAR(50) | 'indicTrans' / 'googleTranslate' / 'none' |
| `timestamp` | DATETIME | Auto-set on creation |

**View chat logs:**
```bash
# Using Django shell
cd backend
python manage.py shell
>>> from chatbot.models import ChatLog
>>> ChatLog.objects.all().values()
```

---

## 14. Future Improvements

| # | Improvement | Benefit |
|---|------------|---------|
| 1 | **Real IndicTrans2 model** | Integrate AI4Bharat IndicTrans2 for better Hindi translation quality |
| 2 | **More languages** | Add Gujarati, Malayalam, Odia, Assamese support |
| 3 | **Rasa custom actions** | Dynamic slot filling for personalized responses |
| 4 | **Admin dashboard** | View and analyze chat logs via Django admin |
| 5 | **Voice input** | Add speech-to-text for accessibility |
| 6 | **Multi-turn conversations** | Remember context across multiple questions |
| 7 | **Larger FAQ** | Expand to 200+ Q&A pairs with richer responses |
| 8 | **PostgreSQL** | Migrate from SQLite to PostgreSQL for production |
| 9 | **Rate limiting** | Add rate limiting middleware to prevent abuse |
| 10 | **Analytics** | Track most-asked questions and unanswered intents |

---

## 15. License

This project was built for educational and demonstration purposes as part of Smart India Hackathon 2025.

```
MIT License — Free to use, modify, and distribute with attribution.
```

---

*Built with ❤️ for Smart India Hackathon 2025 · Problem Statement 25104 · Smart Education*
