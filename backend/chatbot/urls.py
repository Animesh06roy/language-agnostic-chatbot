"""
URL Routes for the Chatbot App

/api/chat/     — Main chat endpoint (POST: send message, GET: health check)
/api/history/  — View recent chat logs (GET)
"""

from django.urls import path
from chatbot.views import ChatView, ChatHistoryView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('history/', ChatHistoryView.as_view(), name='history'),
]
