"""
Rasa NLU Client

Sends text to Rasa server for:
  - Intent classification (e.g. 'ask_admission_process')
  - Slot filling / entity extraction (e.g. {semester: "3rd"})

Falls back to a keyword-based classifier if Rasa is not running.
Uses WORD BOUNDARY matching (not substring) to avoid false positives.
e.g. "tc" should NOT match inside "contact", "hi" should NOT match inside "this"
"""

import re
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# Keyword → intent mapping
# IMPORTANT: matching uses word boundaries (\\b), not substring search
KEYWORD_INTENT_MAP = {
    # ── Greetings ─────────────────────────────────────────────────────────────
    "hello": "greet",
    "hi": "greet",
    "hey": "greet",
    "good morning": "greet",
    "good afternoon": "greet",
    "good evening": "greet",
    "namaste": "greet",
    "namaskar": "greet",
    "thanks": "greet",
    "thank you": "greet",

    # ── Admissions ────────────────────────────────────────────────────────────
    "admission": "ask_admission_process",
    "admissions": "ask_admission_process",
    "enroll": "ask_admission_process",
    "enrollment": "ask_admission_process",
    "joining": "ask_admission_process",
    "deadline": "ask_admission_deadline",
    "last date": "ask_admission_deadline",
    "eligibility": "ask_admission_eligibility",
    "eligible": "ask_admission_eligibility",
    "qualification": "ask_admission_eligibility",
    "documents required": "ask_admission_documents",
    "required documents": "ask_admission_documents",
    "certificates needed": "ask_admission_documents",
    "application status": "ask_admission_status",

    # ── Scholarships ──────────────────────────────────────────────────────────
    "scholarship": "ask_scholarship_available",
    "scholarships": "ask_scholarship_available",
    "merit scholarship": "ask_scholarship_merit",
    "scholarship amount": "ask_scholarship_amount",
    "financial aid": "ask_scholarship_available",

    # ── Hostel ────────────────────────────────────────────────────────────────
    "hostel": "ask_hostel_available",
    "hostel fee": "ask_hostel_fees",
    "hostel fees": "ask_hostel_fees",
    "hostel rules": "ask_hostel_rules",
    "hostel facilities": "ask_hostel_facilities",
    "accommodation": "ask_hostel_available",
    "dormitory": "ask_hostel_available",

    # ── Attendance ────────────────────────────────────────────────────────────
    "attendance": "ask_attendance_required",
    "attendance shortage": "ask_attendance_shortage",
    "short attendance": "ask_attendance_shortage",
    "condonation": "ask_attendance_condonation",

    # ── Exams ─────────────────────────────────────────────────────────────────
    "exam schedule": "ask_exam_schedule",
    "exam timetable": "ask_exam_schedule",
    "semester exam": "ask_exam_schedule",
    "examination": "ask_exam_schedule",
    "exam date": "ask_exam_schedule",
    "when are exams": "ask_exam_schedule",
    "hall ticket": "ask_exam_hall_ticket",
    "admit card": "ask_exam_hall_ticket",
    "revaluation": "ask_exam_revaluation",
    "exam result": "ask_exam_result",
    "semester result": "ask_exam_result",
    "backlog": "ask_exam_backlog",
    "arrear": "ask_exam_backlog",
    "supplementary exam": "ask_exam_backlog",
    "exam materials": "ask_exam_materials",

    # ── Library ───────────────────────────────────────────────────────────────
    "library": "ask_library_timing",
    "borrow books": "ask_library_books",
    "library books": "ask_library_books",
    "library membership": "ask_library_membership",
    "ebooks": "ask_library_ebooks",
    "digital library": "ask_library_ebooks",

    # ── Fees ──────────────────────────────────────────────────────────────────
    "fee structure": "ask_fee_structure",
    "tuition fee": "ask_fee_structure",
    "college fees": "ask_fee_structure",
    "annual fee": "ask_fee_structure",
    "fee payment": "ask_fee_payment",
    "pay fees": "ask_fee_payment",
    "fee deadline": "ask_fee_deadline",
    "fee receipt": "ask_fee_receipt",
    "fee installment": "ask_fee_installment",
    "installment": "ask_fee_installment",

    # ── Leave ─────────────────────────────────────────────────────────────────
    "leave application": "ask_leave_apply",
    "apply for leave": "ask_leave_apply",
    "medical leave": "ask_leave_medical",
    "sick leave": "ask_leave_medical",
    "casual leave": "ask_leave_casual",

    # ── Placements ────────────────────────────────────────────────────────────
    "placement": "ask_placement_process",
    "placements": "ask_placement_process",
    "campus recruitment": "ask_placement_process",
    "placement eligibility": "ask_placement_eligibility",
    "recruiting companies": "ask_placement_companies",
    "companies visiting": "ask_placement_companies",
    "placement package": "ask_placement_package",
    "average package": "ask_placement_package",
    "highest package": "ask_placement_package",
    "salary package": "ask_placement_package",
    "placement preparation": "ask_placement_preparation",

    # ── Faculty ───────────────────────────────────────────────────────────────
    "faculty contact": "ask_faculty_contact",
    "professor contact": "ask_faculty_contact",
    "office hours": "ask_faculty_office_hours",
    "consultation hours": "ask_faculty_office_hours",
    "head of department": "ask_faculty_hod",

    # ── Canteen ───────────────────────────────────────────────────────────────
    "canteen": "ask_canteen_timing",
    "cafeteria": "ask_canteen_timing",
    "canteen menu": "ask_canteen_menu",
    "food menu": "ask_canteen_menu",

    # ── Sports ────────────────────────────────────────────────────────────────
    "sports facilities": "ask_sports_facilities",
    "sports ground": "ask_sports_facilities",
    "sports tryout": "ask_sports_tryouts",
    "team tryout": "ask_sports_tryouts",

    # ── General ───────────────────────────────────────────────────────────────
    "college timing": "ask_college_timing",
    "college hours": "ask_college_timing",
    "college time": "ask_college_timing",
    "principal contact": "ask_principal_contact",
    "wifi": "ask_wifi_access",
    "wi-fi": "ask_wifi_access",
    "college internet": "ask_wifi_access",
    "transfer certificate": "ask_tc_bonafide",
    "bonafide certificate": "ask_tc_bonafide",
    "internship": "ask_internship",
    "anti ragging": "ask_anti_ragging",
    "ragging": "ask_anti_ragging",
}

# Single-word keywords that need EXACT word-boundary matching
# These are safe to match as whole words only
SINGLE_WORD_KEYWORDS = {
    "hello": "greet",
    "hi": "greet",
    "hey": "greet",
    "namaste": "greet",
    "namaskar": "greet",
    "thanks": "greet",
    "admission": "ask_admission_process",
    "admissions": "ask_admission_process",
    "scholarship": "ask_scholarship_available",
    "scholarships": "ask_scholarship_available",
    "hostel": "ask_hostel_available",
    "accommodation": "ask_hostel_available",
    "attendance": "ask_attendance_required",
    "examination": "ask_exam_schedule",
    "revaluation": "ask_exam_revaluation",
    "backlog": "ask_exam_backlog",
    "arrear": "ask_exam_backlog",
    "library": "ask_library_timing",
    "ebooks": "ask_library_ebooks",
    "installment": "ask_fee_installment",
    "placement": "ask_placement_process",
    "placements": "ask_placement_process",
    "canteen": "ask_canteen_timing",
    "cafeteria": "ask_canteen_timing",
    "wifi": "ask_wifi_access",
    "internship": "ask_internship",
    "ragging": "ask_anti_ragging",
}


def classify_intent(text: str) -> dict:
    """
    Classify the intent of the given English text.
    Tries Rasa first, then falls back to keyword classifier.
    """
    rasa_result = _call_rasa(text)
    if rasa_result:
        return rasa_result

    logger.warning("Rasa not available — using keyword fallback classifier")
    return _keyword_classify(text)


def _call_rasa(text: str) -> dict | None:
    """Call Rasa NLU REST API. Returns None if Rasa is not running."""
    try:
        url = f"{settings.RASA_SERVER_URL}/model/parse"
        payload = {"text": text}
        response = requests.post(url, json=payload, timeout=2)

        if response.status_code == 200:
            data = response.json()
            intent_data = data.get("intent", {})
            entities = data.get("entities", [])
            return {
                "intent": intent_data.get("name", "unknown"),
                "confidence": round(intent_data.get("confidence", 0.0), 3),
                "entities": entities,
                "source": "rasa",
            }
    except requests.exceptions.ConnectionError:
        logger.info("Rasa server not running — using fallback")
    except requests.exceptions.Timeout:
        logger.warning("Rasa server timed out — using fallback")
    except Exception as e:
        logger.error(f"Rasa call error: {e}")

    return None


def _keyword_classify(text: str) -> dict:
    """
    Keyword-based intent classifier with WORD BOUNDARY matching.

    Uses \\b regex word boundaries so:
      - "hi"  matches "hi" and "Hi" but NOT "this" or "history"
      - "tc"  matches "tc" only, NOT "contact" or "atch"
      - "fee" matches "fee" only, NOT "coffee" or "referee"
    """
    text_lower = text.lower().strip()

    # Step 1: Check multi-word phrases first (more specific, plain substring is OK
    # because multi-word phrases won't accidentally match inside other words)
    best_intent = "unknown"
    best_match_len = 0

    for keyword, intent in KEYWORD_INTENT_MAP.items():
        word_count = len(keyword.split())
        if word_count >= 2:
            # Multi-word phrase: safe to use plain substring match
            if keyword in text_lower and len(keyword) > best_match_len:
                best_intent = intent
                best_match_len = len(keyword)

    if best_intent != "unknown":
        logger.info(f"[Fallback] Multi-word match: '{text}' → {best_intent}")
        return {"intent": best_intent, "confidence": 0.85, "entities": [], "source": "fallback"}

    # Step 2: Single-word keywords — use regex word boundary \b to avoid
    # matching "hi" inside "this", "tc" inside "contact", etc.
    for keyword, intent in SINGLE_WORD_KEYWORDS.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            logger.info(f"[Fallback] Word-boundary match: '{keyword}' in '{text}' → {intent}")
            return {"intent": intent, "confidence": 0.85, "entities": [], "source": "fallback"}

    logger.info(f"[Fallback] No match for: '{text}' → unknown")
    return {"intent": "unknown", "confidence": 0.0, "entities": [], "source": "fallback"}
