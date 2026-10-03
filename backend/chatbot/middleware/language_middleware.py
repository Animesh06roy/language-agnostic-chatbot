"""
Language Middleware

This middleware intercepts every request to the /api/chat/ endpoint and:
1. Detects the language of the incoming query
2. Performs translation (IndicTrans for Hindi, Google Translate for others)
3. Attaches the detected language and translated text to the request object
4. Logs the interaction to SQLite via Django ORM

CV reference:
  "Engineered Django middleware intercepting every query for language detection
   and translation before it reached the intent engine"

NOTE: The actual translation and logging happens in the view,
because we need the full response (intent + answer) to log.
This middleware attaches language detection metadata to the request.
"""

import logging
from chatbot.translation_service import detect_language

logger = logging.getLogger(__name__)


class LanguageMiddleware:
    """
    Django middleware that intercepts incoming requests.
    For chat API requests, it pre-detects the language and
    attaches it to the request object for use in views.
    """

    def __init__(self, get_response):
        # Django calls this once at startup
        self.get_response = get_response

    def __call__(self, request):
        # Process request BEFORE the view
        self._process_request(request)

        # Let the request continue to the view
        response = self.get_response(request)

        # We could post-process the response here too
        return response

    def _process_request(self, request):
        """
        If this is a POST request to the chat endpoint,
        detect the language from the query body.
        """
        if request.method == 'POST' and '/api/chat/' in request.path:
            try:
                import json
                body = json.loads(request.body.decode('utf-8'))
                user_message = body.get('message', '')

                if user_message:
                    # Detect language and attach to request
                    lang_info = detect_language(user_message)
                    request.detected_language = lang_info

                    logger.info(
                        f"[Middleware] Intercepted request — "
                        f"Language: {lang_info['name']} ({lang_info['code']}) — "
                        f"Query: '{user_message[:50]}'"
                    )
                else:
                    request.detected_language = {'code': 'en', 'name': 'English'}

            except Exception as e:
                logger.error(f"[Middleware] Language detection error: {e}")
                request.detected_language = {'code': 'en', 'name': 'English'}
        else:
            # For non-chat requests, just pass through
            request.detected_language = None
