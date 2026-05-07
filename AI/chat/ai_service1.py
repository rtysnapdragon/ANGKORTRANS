

import google.generativeai as genai
import os
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_AI_API_KEY)

def call_gemini(prompt: str):
    model = genai.GenerativeModel("gemini-3-flash-preview")

    response = model.generate_content(prompt)

    return response.text