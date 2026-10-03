"""
Chat API Views

The /api/chat/ endpoint implements the full 10-step NLP pipeline:

Step 1:  Receive user query
Step 2:  Detect language (via middleware + translation_service)
Step 3:  If Hindi → IndicTrans
Step 4:  Else → Google Translate
Step 5:  Translate to English
Step 6:  Pass English text to Rasa NLU
Step 7:  Rasa predicts intent + entities
Step 8:  Retrieve answer from FAQ knowledge base
Step 9:  Translate answer back to user's language
Step 10: Return response with metadata

CV reference: "10-step NLP pipeline", "50+ FAQ intents", "<2s end-to-end latency"
"""

import logging
import time
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from chatbot.translation_service import (
    detect_language,
    translate_to_english,
    translate_from_english,
)
from chatbot.rasa_client import classify_intent
from chatbot.faq_knowledge_base import get_answer
from chatbot.models import ChatLog

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    """
    Main chatbot API endpoint.
    POST /api/chat/
    
    Request body:  { "message": "What are the hostel fees?" }
    Response body: {
        "response": "Hostel fees are ...",
        "detected_language": "English",
        "language_code": "en",
        "intent": "ask_hostel_fees",
        "confidence": 0.85,
        "english_query": "What are the hostel fees?",
        "translation_method": "none",
        "processing_time_ms": 120
    }
    """

    def post(self, request):
        """Handle incoming chat message — full 10-step pipeline."""
        start_time = time.time()

        # ── Parse Request ────────────────────────────────────────────────────
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_message = body.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        logger.info(f"[Pipeline] STEP 1 — Received: '{user_message}'")

        # ── STEP 2: Language Detection ───────────────────────────────────────
        # Middleware already detected it; use that result if available
        lang_info = getattr(request, 'detected_language', None)
        if not lang_info:
            lang_info = detect_language(user_message)

        source_lang = lang_info['code']
        lang_name = lang_info['name']
        logger.info(f"[Pipeline] STEP 2 — Language: {lang_name} ({source_lang})")

        # ── STEPS 3 & 4: Translation to English ─────────────────────────────
        # Step 3: Hindi → IndicTrans
        # Step 4: Other → Google Translate
        # Step 5: Result is English text
        translation_result = translate_to_english(user_message, source_lang)
        english_query = translation_result['translated_text']
        translation_method = translation_result['method']
        logger.info(f"[Pipeline] STEP 3/4/5 — English: '{english_query}' via {translation_method}")

        # ── STEP 6 & 7: Rasa NLU ────────────────────────────────────────────
        # Step 6: Pass English text to Rasa
        # Step 7: Rasa predicts intent + entities (slot filling)
        rasa_result = classify_intent(english_query)
        intent = rasa_result['intent']
        confidence = rasa_result['confidence']
        entities = rasa_result['entities']
        logger.info(f"[Pipeline] STEP 6/7 — Intent: {intent} ({confidence}), Source: {rasa_result['source']}")

        # ── STEP 8: FAQ Retrieval ────────────────────────────────────────────
        english_answer = get_answer(intent)
        logger.info(f"[Pipeline] STEP 8 — Retrieved FAQ answer for intent: {intent}")

        # ── STEP 9: Translate Response Back ──────────────────────────────────
        final_response = translate_from_english(english_answer, source_lang)
        logger.info(f"[Pipeline] STEP 9 — Translated response back to {lang_name}")

        # ── STEP 10: Log to SQLite ────────────────────────────────────────────
        ChatLog.objects.create(
            original_query=user_message,
            detected_language=source_lang,
            language_name=lang_name,
            english_query=english_query,
            intent=intent,
            intent_confidence=confidence,
            response=final_response,
            translation_method=translation_method,
        )
        logger.info(f"[Pipeline] STEP 10 — Interaction logged to SQLite")

        # Calculate processing time
        processing_time_ms = round((time.time() - start_time) * 1000, 1)
        logger.info(f"[Pipeline] COMPLETE — {processing_time_ms}ms")

        return JsonResponse({
            'response': final_response,
            'detected_language': lang_name,
            'language_code': source_lang,
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'english_query': english_query,
            'translation_method': translation_method,
            'processing_time_ms': processing_time_ms,
        })

    def get(self, request):
        """Health check endpoint."""
        return JsonResponse({
            'status': 'ok',
            'message': 'Language Agnostic AI Chatbot — SIH 2025',
            'version': '1.0.0',
        })


@method_decorator(csrf_exempt, name='dispatch')
class ChatHistoryView(View):
    """
    GET /api/history/
    Returns recent chat logs from SQLite for debugging.
    """

    def get(self, request):
        """Return last 20 chat interactions."""
        logs = ChatLog.objects.all()[:20]
        data = [
            {
                'id': log.id,
                'original_query': log.original_query,
                'detected_language': log.language_name,
                'language_code': log.detected_language,
                'english_query': log.english_query,
                'intent': log.intent,
                'confidence': log.intent_confidence,
                'response': log.response,
                'translation_method': log.translation_method,
                'timestamp': log.timestamp.isoformat(),
            }
            for log in logs
        ]
        return JsonResponse({'logs': data, 'count': len(data)})
