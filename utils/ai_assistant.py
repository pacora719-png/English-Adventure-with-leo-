# utils/ai_assistant.py
import random

class AIAssistant:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def get_response(self, user_message, context):
        responses = [
            "¡Qué interesante! ¿Quieres aprender más? 📚",
            "¡Me encanta que estés aprendiendo! 🦁",
            "¡Excelente pregunta! Sigue así 🌟",
            "¡Tú puedes! Cada día aprendes más 🎉"
        ]
        return random.choice(responses)
