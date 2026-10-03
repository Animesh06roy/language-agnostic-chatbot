"""
Generate Project Documentation PDF
Language Agnostic AI Chatbot — Smart India Hackathon 2025
5 pages covering: Overview, Architecture, How it works, Tech Stack, How to Run
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Colors ────────────────────────────────────────────────────────────────────
INDIGO     = colors.HexColor('#4F46E5')
INDIGO_DARK = colors.HexColor('#3730A3')
SLATE_800  = colors.HexColor('#1E293B')
SLATE_600  = colors.HexColor('#475569')
SLATE_200  = colors.HexColor('#E2E8F0')
SLATE_50   = colors.HexColor('#F8FAFC')
ORANGE     = colors.HexColor('#EA580C')
GREEN      = colors.HexColor('#16A34A')
WHITE      = colors.white


def build_styles():
    """Define custom paragraph styles."""
    base = getSampleStyleSheet()

    styles = {}

    styles['PageTitle'] = ParagraphStyle(
        'PageTitle',
        fontSize=22,
        fontName='Helvetica-Bold',
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=4,
        leading=28,
    )

    styles['PageSubtitle'] = ParagraphStyle(
        'PageSubtitle',
        fontSize=10,
        fontName='Helvetica',
        textColor=colors.HexColor('#C7D2FE'),
        alignment=TA_LEFT,
        spaceAfter=0,
    )

    styles['SectionHeading'] = ParagraphStyle(
        'SectionHeading',
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=INDIGO_DARK,
        spaceBefore=16,
        spaceAfter=6,
        borderPad=0,
    )

    styles['SubHeading'] = ParagraphStyle(
        'SubHeading',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=SLATE_800,
        spaceBefore=10,
        spaceAfter=4,
    )

    styles['Body'] = ParagraphStyle(
        'Body',
        fontSize=9.5,
        fontName='Helvetica',
        textColor=SLATE_600,
        spaceBefore=3,
        spaceAfter=3,
        leading=15,
        alignment=TA_JUSTIFY,
    )

    styles['Bullet'] = ParagraphStyle(
        'Bullet',
        fontSize=9.5,
        fontName='Helvetica',
        textColor=SLATE_600,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=14,
        leading=14,
    )

    styles['Code'] = ParagraphStyle(
        'Code',
        fontSize=8.5,
        fontName='Courier',
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=10,
        leading=13,
        backColor=SLATE_50,
    )

    styles['StepNumber'] = ParagraphStyle(
        'StepNumber',
        fontSize=9.5,
        fontName='Helvetica-Bold',
        textColor=INDIGO,
        spaceBefore=4,
        spaceAfter=2,
        leftIndent=0,
        leading=14,
    )

    styles['Footer'] = ParagraphStyle(
        'Footer',
        fontSize=8,
        fontName='Helvetica',
        textColor=colors.HexColor('#94A3B8'),
        alignment=TA_CENTER,
    )

    return styles


def header_block(styles, page_num, title, subtitle):
    """Create the indigo header banner for each page."""
    header_data = [[
        Paragraph(f'<font color="white"><b>{title}</b></font>', styles['PageTitle']),
        Paragraph(f'<font color="#C7D2FE">{subtitle}</font>', styles['PageSubtitle']),
    ]]

    # We use a full-width table as the banner
    header_table = Table(
        [[Paragraph(title, styles['PageTitle'])],
         [Paragraph(subtitle, styles['PageSubtitle'])]],
        colWidths=[17 * cm]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), INDIGO),
        ('TOPPADDING',    (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('LEFTPADDING',   (0, 0), (-1, -1), 20),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 20),
        ('ROUNDEDCORNERS', [8]),
    ]))
    return header_table


def divider():
    return HRFlowable(width='100%', thickness=1, color=SLATE_200, spaceAfter=8, spaceBefore=8)


def bullet(styles, text):
    return Paragraph(f'• &nbsp; {text}', styles['Bullet'])


def step(styles, num, text):
    return Paragraph(f'<b>Step {num}.</b> &nbsp; {text}', styles['StepNumber'])


def make_table(data, col_widths, header_bg=INDIGO):
    """Utility to create a styled table."""
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 9),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (-1, -1), SLATE_600),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, SLATE_50]),
        ('GRID',          (0, 0), (-1, -1), 0.5, SLATE_200),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def generate_pdf(output_path: str):
    """Generate the complete 5-page project PDF."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Language Agnostic AI Chatbot — SIH 2025",
        author="Smart India Hackathon 2025",
        subject="Problem Statement 25104 — Smart Education",
    )

    S = build_styles()
    story = []

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 1: Project Overview
    # ─────────────────────────────────────────────────────────────────────────
    story.append(header_block(S, 1,
        "Language Agnostic AI Chatbot",
        "Smart India Hackathon 2025  ·  Problem Statement 25104  ·  Smart Education Theme"
    ))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Project Overview", S['SectionHeading']))
    story.append(divider())
    story.append(Paragraph(
        "This project is a multilingual education FAQ chatbot built for Smart India Hackathon 2025. "
        "It enables students to ask questions about college services in any Indian language — Hindi, Tamil, Telugu, "
        "Malayalam, Bengali, and more — and receive accurate answers in their own language. "
        "The system removes the language barrier from accessing institutional information.",
        S['Body']
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Problem Statement", S['SubHeading']))
    story.append(Paragraph(
        "Indian educational institutions serve students who are more comfortable communicating "
        "in their native language. Existing FAQ systems are English-only, creating an "
        "accessibility gap. Problem Statement 25104 challenges teams to build AI tools that "
        "democratize access to educational information across language barriers.",
        S['Body']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Key Features", S['SubHeading']))

    features = [
        ["#", "Feature", "Description"],
        ["1", "Language Detection", "Identifies user's language automatically using langdetect"],
        ["2", "IndicTrans Routing", "Hindi queries routed through IndicTrans pipeline"],
        ["3", "Google Translate", "All other languages handled via Google Translate API"],
        ["4", "English NLU", "Normalizes all queries to English before intent classification"],
        ["5", "Rasa NLU", "Classifies intent and extracts entities (slot filling)"],
        ["6", "FAQ Retrieval", "55+ Q&A pairs across 12 education categories"],
        ["7", "Response Translation", "Answers translated back to the user's language"],
        ["8", "Audit Logging", "Every interaction logged to SQLite via Django ORM"],
        ["9", "Clean Chat UI", "Responsive React + Tailwind interface with pipeline metadata"],
        ["10", "< 2s Response", "End-to-end latency target: under 2 seconds on localhost"],
    ]
    story.append(make_table(features, [0.8*cm, 4.5*cm, 11.2*cm]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("FAQ Categories", S['SubHeading']))

    cats = [
        "Admissions", "Scholarships", "Hostel & Accommodation", "Attendance",
        "Examinations", "Library", "Fees", "Leave Policy",
        "Placements", "Faculty", "Canteen & Sports", "General / Administration"
    ]
    for i in range(0, len(cats), 3):
        row = cats[i:i+3]
        story.append(Paragraph(
            " &nbsp;&nbsp;&nbsp; ".join(f"● {c}" for c in row),
            S['Body']
        ))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 2: Architecture Diagram
    # ─────────────────────────────────────────────────────────────────────────
    story.append(header_block(S, 2,
        "System Architecture",
        "Three-tier architecture: React Frontend → Django Backend → Rasa NLU + SQLite"
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Architecture Overview", S['SectionHeading']))
    story.append(divider())

    # Architecture table (visual representation)
    arch_data = [
        ["Layer", "Component", "Technology", "Port"],
        ["Frontend", "Chat UI", "React 19 + TypeScript + Tailwind CSS", "3000"],
        ["Backend", "API Server", "Python + Django 4.2 + Django REST Framework", "8000"],
        ["Backend", "Language Middleware", "langdetect + deep-translator (auto-routing)", "—"],
        ["Backend", "NLU Client", "Rasa HTTP client + keyword fallback classifier", "—"],
        ["Backend", "ORM & Logging", "Django ORM → SQLite (ChatLog model)", "—"],
        ["NLU Server", "Intent Classification", "Rasa 3.x — DIET Classifier + Entity Extractor", "5005"],
        ["Database", "Interaction Logs", "SQLite (db.sqlite3) — auto-created on first run", "—"],
    ]
    story.append(make_table(arch_data, [2.8*cm, 4*cm, 7.2*cm, 2.5*cm]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Request Flow (ASCII Architecture Diagram)", S['SubHeading']))

    arch_lines = [
        "┌─────────────────────────────────────────────────────────────┐",
        "│  BROWSER  ──►  React App (localhost:3000)                   │",
        "│                                                             │",
        "│  User types: 'hostel ki fees kya hai?' (Hindi)             │",
        "│                 │  POST /api/chat/                          │",
        "└─────────────────┼───────────────────────────────────────────┘",
        "                  ▼",
        "┌─────────────────────────────────────────────────────────────┐",
        "│  DJANGO BACKEND (localhost:8000)                            │",
        "│                                                             │",
        "│  LanguageMiddleware  →  detects 'hi' (Hindi)               │",
        "│         │                                                   │",
        "│         ▼                                                   │",
        "│  ChatView                                                   │",
        "│   ├─ IndicTrans  →  'what are the hostel fees?'            │",
        "│   ├─ Rasa NLU    →  intent: ask_hostel_fees                │",
        "│   ├─ FAQ Lookup  →  'Hostel fees are Rs.40,000/year...'    │",
        "│   ├─ IndicTrans  →  'हॉस्टल की फीस 40,000 रुपये है...'    │",
        "│   └─ SQLite Log  →  stores all fields via Django ORM       │",
        "│         │                                                   │",
        "│         ▼   (if Rasa not running → keyword fallback)       │",
        "│  Rasa Server (localhost:5005) ──── SQLite (db.sqlite3)     │",
        "└─────────────────────────────────────────────────────────────┘",
        "                  │  JSON Response",
        "                  ▼",
        "┌─────────────────────────────────────────────────────────────┐",
        "│  BROWSER  ◄──  Response displayed in user's language       │",
        "└─────────────────────────────────────────────────────────────┘",
    ]

    for line in arch_lines:
        story.append(Paragraph(line, S['Code']))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Fallback Behavior:</b> If the Rasa server is not running, a keyword-based "
        "classifier automatically handles intent detection. This means the demo works "
        "end-to-end without requiring Rasa to be installed.",
        S['Body']
    ))

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 3: How the Chatbot Works (Step-by-step)
    # ─────────────────────────────────────────────────────────────────────────
    story.append(header_block(S, 3,
        "How the Chatbot Works",
        "10-step NLP pipeline from user input to multilingual response"
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("The 10-Step NLP Pipeline", S['SectionHeading']))
    story.append(divider())

    steps = [
        ("1", "User Input",
         "The user types a question in any supported language into the React chat interface. "
         "The message is sent via HTTP POST to /api/chat/ on the Django backend."),
        ("2", "Language Detection",
         "Django's LanguageMiddleware intercepts the request and calls langdetect.detect() "
         "to identify the language. Returns an ISO 639-1 code (e.g. 'hi' = Hindi, 'ta' = Tamil)."),
        ("3", "Hindi → IndicTrans",
         "If the detected language is Hindi ('hi'), the query is routed through the IndicTrans "
         "pipeline — AI4Bharat's translation model for Indian languages. In the demo, "
         "deep-translator handles the translation while preserving the routing logic."),
        ("4", "Other → Google Translate",
         "For all other supported languages (Tamil, Telugu, Bengali, etc.), the query is "
         "sent to Google Translate via the deep-translator library to produce an English translation."),
        ("5", "English Text",
         "The result of Steps 3 or 4 is a clean English sentence that captures the user's "
         "intent. If the user typed in English, no translation is needed (method = 'none')."),
        ("6", "Pass to Rasa NLU",
         "The English text is sent via HTTP POST to the Rasa NLU server at "
         "localhost:5005/model/parse. Rasa's DIET Classifier processes the text."),
        ("7", "Intent + Slot Filling",
         "Rasa returns an intent name (e.g. ask_hostel_fees) and extracted entities "
         "(e.g. semester: '3rd', subject: 'mathematics'). Confidence scores are also returned."),
        ("8", "FAQ Retrieval",
         "The intent name is used to look up the answer in the FAQ knowledge base — a "
         "Python dict of 55 intent → answer mappings covering 12 education categories."),
        ("9", "Translate Response Back",
         "The English answer is translated back to the user's original language using the "
         "same routing: IndicTrans for Hindi, Google Translate for others, no-op for English."),
        ("10", "Log & Return",
         "The interaction (original query, language, English query, intent, confidence, "
         "response, translation method, timestamp) is saved to SQLite via Django ORM. "
         "The JSON response is returned to React for display."),
    ]

    for num, title, desc in steps:
        story.append(KeepTogether([
            Paragraph(f"<b>Step {num}: {title}</b>", S['StepNumber']),
            Paragraph(desc, S['Body']),
            Spacer(1, 4),
        ]))

    story.append(Spacer(1, 8))

    # Mini flow diagram
    flow_items = [
        "User (any language)",
        "Language Detection (langdetect)",
        "Translation to English (IndicTrans / Google Translate)",
        "Rasa NLU Intent Classification + Slot Filling",
        "FAQ Knowledge Base Retrieval",
        "Translate Response Back (IndicTrans / Google Translate)",
        "Display Response to User",
    ]

    flow_data = [[Paragraph(f"<b>{i+1}.</b>  {item}", S['Body'])] for i, item in enumerate(flow_items)]
    ft = Table(flow_data, colWidths=[16.5*cm])
    ft.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [SLATE_50, WHITE]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, SLATE_200),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, SLATE_200),
    ]))
    story.append(ft)

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 4: Technologies Used
    # ─────────────────────────────────────────────────────────────────────────
    story.append(header_block(S, 4,
        "Technologies Used",
        "Why each technology was chosen for this project"
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Technology Choices", S['SectionHeading']))
    story.append(divider())

    tech_choices = [
        ("Django", "Backend Framework",
         "Django provides a clean MVC structure, built-in ORM for SQLite, "
         "and a middleware system that is perfect for intercepting and processing "
         "every request. Its REST Framework makes building the JSON API trivial. "
         "It is widely used in Indian tech companies, making it relevant to showcase."),
        ("React + TypeScript", "Frontend Framework",
         "React's component model keeps the UI code clean and maintainable. "
         "TypeScript adds type safety that prevents runtime errors. "
         "The combination is the industry standard for modern web frontends."),
        ("SQLite", "Database",
         "SQLite requires zero configuration — it creates a single file (db.sqlite3) "
         "on first run. Django's ORM handles all queries, making the code database-agnostic. "
         "Perfect for a hackathon demo that should 'just work' on any machine."),
        ("Rasa", "NLU Engine",
         "Rasa is an open-source NLU framework that can be trained locally without "
         "an internet connection. Its DIET Classifier handles intent detection and "
         "entity extraction (slot filling) — exactly what was described in the problem statement. "
         "Rasa is used in production by large educational platforms."),
        ("Google Translate (deep-translator)", "Translation",
         "deep-translator wraps the Google Translate API in a clean Python interface. "
         "Google Translate supports 130+ languages including all major Indian languages, "
         "making it the right choice for the fallback translation path."),
        ("IndicTrans", "Hindi Translation",
         "AI4Bharat's IndicTrans2 is a state-of-the-art translation model specifically "
         "trained on Indian language pairs. For Hindi, it significantly outperforms "
         "general-purpose translators on colloquial and domain-specific text. "
         "The demo routes Hindi through this pipeline as described in the CV."),
        ("langdetect", "Language Detection",
         "Google's language-detection algorithm ported to Python. Accurately identifies "
         "55+ languages with high confidence. It works offline (no API calls needed) "
         "and adds negligible latency to the pipeline."),
        ("Tailwind CSS", "Styling",
         "Utility-first CSS framework that enables rapid UI development without "
         "writing custom CSS files. The responsive design works on mobile and desktop. "
         "No context-switching between CSS and HTML during development."),
    ]

    for tech, role, reason in tech_choices:
        story.append(KeepTogether([
            Paragraph(f"<b>{tech}</b> — <i>{role}</i>", S['SubHeading']),
            Paragraph(reason, S['Body']),
            Spacer(1, 4),
        ]))

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE 5: How to Run
    # ─────────────────────────────────────────────────────────────────────────
    story.append(header_block(S, 5,
        "How to Run the Project",
        "Installation, setup, and startup commands for all three services"
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Prerequisites", S['SectionHeading']))
    story.append(divider())

    for item in ["Python 3.10 or higher", "Node.js 18 or higher", "npm 9 or higher",
                 "pip (Python package manager)"]:
        story.append(bullet(S, item))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Folder Structure (Summary)", S['SubHeading']))

    fs_data = [
        ["Folder / File", "Purpose"],
        ["backend/", "Django server — API, middleware, models, FAQ"],
        ["frontend/", "React + TypeScript + Tailwind chat interface"],
        ["rasa_bot/", "Rasa NLU config, training data, domain"],
        ["dataset/faq_dataset.csv", "55 Q&A pairs used for Rasa training"],
        ["backend/requirements.txt", "Python dependencies"],
        ["frontend/package.json", "Node.js dependencies"],
        ["backend/db.sqlite3", "Auto-created SQLite database"],
        ["README.md", "Full documentation"],
    ]
    story.append(make_table(fs_data, [7*cm, 9.5*cm]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Step-by-step Setup", S['SectionHeading']))
    story.append(divider())

    story.append(Paragraph("1. Install Python dependencies", S['SubHeading']))
    for line in [
        "cd backend",
        "python3 -m venv venv",
        "source venv/bin/activate   # Windows: venv\\Scripts\\activate",
        "pip install -r requirements.txt",
    ]:
        story.append(Paragraph(line, S['Code']))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Set up and run Django backend", S['SubHeading']))
    for line in [
        "python manage.py migrate        # creates db.sqlite3",
        "python manage.py runserver      # starts on localhost:8000",
    ]:
        story.append(Paragraph(line, S['Code']))

    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Run the React frontend", S['SubHeading']))
    for line in [
        "cd ../frontend",
        "npm install",
        "npm run dev                      # starts on localhost:3000",
    ]:
        story.append(Paragraph(line, S['Code']))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. (Optional) Run Rasa NLU server", S['SubHeading']))
    for line in [
        "pip install rasa",
        "cd ../rasa_bot",
        "rasa train                       # trains the NLU model",
        "rasa run --enable-api            # starts on localhost:5005",
    ]:
        story.append(Paragraph(line, S['Code']))

    story.append(Paragraph(
        "<b>Note:</b> Rasa is optional. If it is not running, the backend automatically "
        "uses a keyword-based fallback classifier. The app works fully without Rasa.",
        S['Body']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Testing the API", S['SubHeading']))
    for line in [
        '# Health check',
        'curl http://localhost:8000/api/chat/',
        '',
        '# Send a message',
        'curl -X POST http://localhost:8000/api/chat/ \\',
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"message": "What are the hostel fees?"}\'',
    ]:
        story.append(Paragraph(line if line else '&nbsp;', S['Code']))

    story.append(Spacer(1, 10))

    # Summary table
    summary = [
        ["Service", "Command", "URL"],
        ["Django Backend", "python manage.py runserver", "http://localhost:8000"],
        ["React Frontend", "npm run dev", "http://localhost:3000"],
        ["Rasa NLU", "rasa run --enable-api", "http://localhost:5005"],
    ]
    story.append(Paragraph("Quick Reference", S['SubHeading']))
    story.append(make_table(summary, [4*cm, 7*cm, 5.5*cm]))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width='100%', thickness=1, color=SLATE_200))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Language Agnostic AI Chatbot  ·  Smart India Hackathon 2025  ·  PS-25104  ·  Smart Education",
        S['Footer']
    ))

    # Build the PDF
    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == '__main__':
    generate_pdf('/home/claude/language-agnostic-chatbot/docs/project_documentation.pdf')
