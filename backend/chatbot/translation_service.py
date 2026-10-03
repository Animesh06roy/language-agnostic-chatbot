"""
Language Detection and Translation Service

This module handles:
1. Language detection using langdetect
2. IndicTrans simulation for Hindi (auto-routed)
3. Google Translate (via deep-translator) for other Indian languages
4. Fallback to English for unknown languages

CV reference: "auto-routed: IndicTrans for Hindi,
Google Translate fallback for other Indian languages"
"""

import logging
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Mapping of ISO 639-1 codes to human-readable names
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'kn': 'Kannada',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    'or': 'Odia',
    'as': 'Assamese',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'zh-cn': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
}

# Common short English words that langdetect often misidentifies
# If a word is in this set, we force it to English ('en')
COMMON_ENGLISH_WORDS = {
    "hello", "hi", "hey", "ok", "okay", "yes", "no", "thanks",
    "thank", "bye", "help", "start", "what", "when", "where",
    "who", "how", "why", "exam", "fee", "fees", "hostel", "leave",
    "result", "results", "job", "wifi", "tc", "hod", "gym",
    "menu", "food", "room", "marks", "salary", "apply", "admission",
    "scholarship", "placement", "placements", "library", "canteen",
    "attendance", "backlog", "arrear", "faculty", "professor",
}

# Languages where IndicTrans would be used (Indian languages)
INDICNLP_LANGUAGES = {'hi', 'mr', 'bn', 'gu', 'pa', 'or', 'as', 'kn', 'ta', 'te', 'ml'}


def detect_language(text: str) -> dict:
    """
    Detect the language of the input text.

    Special handling:
    - Very short texts (<=3 chars) → assume English (langdetect is unreliable)
    - Known English words → force English to avoid misdetection
    - Otherwise → use langdetect

    Returns a dict with:
      - code: ISO 639-1 language code (e.g. 'hi')
      - name: Human-readable name (e.g. 'Hindi')
    """
    text_stripped = text.strip()

    # Very short input — langdetect is extremely unreliable under 5 characters
    if len(text_stripped) <= 3:
        return {'code': 'en', 'name': 'English'}

    # Known common English single-word inputs
    if text_stripped.lower() in COMMON_ENGLISH_WORDS:
        logger.info(f"[LangDetect] Common English word override: '{text_stripped}' → en")
        return {'code': 'en', 'name': 'English'}

    # Check if ALL characters are ASCII (very likely English or Latin-script)
    # langdetect confuses short ASCII sentences with European languages
    words = text_stripped.split()
    if len(words) <= 2 and all(ord(c) < 128 for c in text_stripped):
        # For short ASCII inputs, try langdetect but default to English on low confidence
        try:
            from langdetect import detect_langs
            results = detect_langs(text_stripped)
            # If top result is not a well-known non-English language with high confidence, use English
            top = results[0]
            if top.prob < 0.85 or top.lang not in LANGUAGE_NAMES:
                logger.info(f"[LangDetect] Low confidence ({top.prob:.2f}) for short text → forcing English")
                return {'code': 'en', 'name': 'English'}
            lang_code = top.lang
        except Exception:
            return {'code': 'en', 'name': 'English'}
    else:
        try:
            lang_code = detect(text_stripped)
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}. Defaulting to English.")
            return {'code': 'en', 'name': 'English'}

    lang_name = LANGUAGE_NAMES.get(lang_code, f'Unknown ({lang_code})')
    logger.info(f"[LangDetect] Detected: {lang_code} ({lang_name}) for '{text_stripped[:40]}'")
    return {
        'code': lang_code,
        'name': lang_name,
    }


def translate_to_english(text: str, source_lang: str) -> dict:
    """
    Translate text to English using the appropriate engine.

    Auto-routing logic (matches CV description):
      - Hindi ('hi')  → IndicTrans pipeline
      - Other Indian languages → Google Translate via deep-translator
      - English → No translation needed
      - Other → Google Translate
    """
    if source_lang == 'en':
        return {'translated_text': text, 'method': 'none'}

    if source_lang == 'hi':
        translated = _indicTrans_to_english(text, source_lang)
        return {'translated_text': translated, 'method': 'indicTrans'}

    translated = _google_translate_to_english(text, source_lang)
    return {'translated_text': translated, 'method': 'googleTranslate'}


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate an English response back to the user's language."""
    if target_lang == 'en':
        return text

    if target_lang == 'hi':
        return _indicTrans_from_english(text, target_lang)

    return _google_translate_from_english(text, target_lang)


# ─── IndicTrans (Hindi) ──────────────────────────────────────────────────────
# NOTE: In production, this would call the AI4Bharat IndicTrans2 API.
# For this demo, we use deep-translator's Google backend as a stand-in,
# but the routing logic (Hindi → IndicTrans) is preserved as per the CV.

def _indicTrans_to_english(text: str, source_lang: str) -> str:
    try:
        logger.info(f"[IndicTrans] Translating '{text[:40]}' from {source_lang} → en")
        translator = GoogleTranslator(source=source_lang, target='en')
        result = translator.translate(text)
        logger.info(f"[IndicTrans] Result: '{result}'")
        return result
    except Exception as e:
        logger.error(f"[IndicTrans] Translation failed: {e}")
        return text


def _indicTrans_from_english(text: str, target_lang: str) -> str:
    try:
        logger.info(f"[IndicTrans] Translating response from en → {target_lang}")
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        return result
    except Exception as e:
        logger.error(f"[IndicTrans] Reverse translation failed: {e}")
        return text


# ─── Google Translate ─────────────────────────────────────────────────────────

def _google_translate_to_english(text: str, source_lang: str) -> str:
    try:
        logger.info(f"[GoogleTranslate] Translating from {source_lang} → en")
        translator = GoogleTranslator(source=source_lang, target='en')
        result = translator.translate(text)
        logger.info(f"[GoogleTranslate] Result: '{result}'")
        return result
    except Exception as e:
        logger.error(f"[GoogleTranslate] Translation failed: {e}")
        return text


def _google_translate_from_english(text: str, target_lang: str) -> str:
    try:
        logger.info(f"[GoogleTranslate] Translating response from en → {target_lang}")
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        return result
    except Exception as e:
        logger.error(f"[GoogleTranslate] Reverse translation failed: {e}")
        return text
