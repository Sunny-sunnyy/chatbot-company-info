"""
API Routes for NMK Chatbot
"""
from api.routes.chat import router as chat_router
from api.routes.chat_openai import router as chat_openai_router
from api.health import router as health_router

__all__ = ["chat_router", "chat_openai_router", "health_router"]
