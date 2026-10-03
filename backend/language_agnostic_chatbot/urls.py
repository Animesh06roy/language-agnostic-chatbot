"""
Main URL Configuration for Language Agnostic AI Chatbot
"""

from django.urls import path, include

urlpatterns = [
    # All chatbot API routes go through /api/
    path('api/', include('chatbot.urls')),
]
