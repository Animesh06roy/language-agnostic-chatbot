"""
Database Model for storing chat interactions.
Every conversation is logged here for audit and analysis.
"""

from django.db import models


class ChatLog(models.Model):
    """
    Stores every chatbot interaction in SQLite.
    Fields match exactly what the CV describes:
      - Original query (in user's language)
      - Detected language
      - English translation
      - Rasa-predicted intent
      - Final response sent to user
      - Timestamp
    """

    # The raw text typed by the user (could be Hindi, Tamil, etc.)
    original_query = models.TextField(
        help_text="Original user query in their language"
    )

    # Language detected (e.g. 'hi' for Hindi, 'ta' for Tamil, 'en' for English)
    detected_language = models.CharField(
        max_length=10,
        help_text="ISO 639-1 language code detected"
    )

    # Human-readable language name (e.g. 'Hindi', 'Tamil')
    language_name = models.CharField(
        max_length=50,
        default='Unknown',
        help_text="Human-readable language name"
    )

    # The English translation passed to Rasa NLU
    english_query = models.TextField(
        help_text="Query translated to English for Rasa"
    )

    # Intent predicted by Rasa (e.g. 'ask_admission', 'ask_fees')
    intent = models.CharField(
        max_length=100,
        default='unknown',
        help_text="Intent predicted by Rasa NLU"
    )

    # Confidence score from Rasa (0.0 to 1.0)
    intent_confidence = models.FloatField(
        default=0.0,
        help_text="Rasa intent confidence score"
    )

    # The final response sent back to the user (in their language)
    response = models.TextField(
        help_text="Response sent to user in their language"
    )

    # Translation method used (indicTrans for Hindi, googleTranslate for others)
    translation_method = models.CharField(
        max_length=50,
        default='none',
        help_text="indicTrans | googleTranslate | none"
    )

    # Auto-set when record is created
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When this interaction happened"
    )

    class Meta:
        ordering = ['-timestamp']  # Newest first
        verbose_name = 'Chat Log'
        verbose_name_plural = 'Chat Logs'

    def __str__(self):
        return f"[{self.timestamp}] {self.detected_language}: {self.original_query[:50]}"
