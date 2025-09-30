from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
from gtts import gTTS
import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

# Gemini model
genai.configure(api_key=settings.GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Keep chat sessions per user in memory
chat_sessions = {}

persona = """You are a divine Navaratri Goddess.
- If the user asks for a story, tell a beautiful Navaratri story in 5–8 sentences.
- Tell positive fortune predictions.
- Otherwise, give blessings in 1–3 sentences.
- Never answer unrelated questions. Guide them back to Navaratri.
- Use divine, compassionate, mystical tone.
"""

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        lang = data.get("lang", "en")
        user_id = str(request.user.id) if request.user.is_authenticated else "guest"

        session_key = f"{user_id}_{lang}"

        if session_key not in chat_sessions:
            if lang == "hi":
                persona_lang = persona + "\n- Always answer in Hindi."
            elif lang == "ta":
                persona_lang = persona + "\n- Always answer in Tamil."
            else:
                persona_lang = persona + "\n- Always answer in English."

            chat_sessions[session_key] = model.start_chat(
                history=[{"role": "user", "parts": [persona_lang]}]
            )

        chat = chat_sessions[session_key]
        response = chat.send_message(user_message)
        reply_text = response.text

        # Audio for Hindi and Tamil
        audio_url = None
        if lang in ["hi", "ta"]:
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            filename = f"{user_id}_{lang}_reply.mp3"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            tts = gTTS(reply_text, lang=lang)
            tts.save(filepath)
            audio_url = f"{settings.MEDIA_URL}{filename}"
            audio_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
            print(audio_url)

        # Story images fetched directly from the internet
        # Story images fetched directly from the internet (direct image URLs)
        story_images = [
            "https://t3.ftcdn.net/jpg/05/89/60/68/360_F_589606850_gwo1VcCfzPNFs209Z2G9HAsQKFYsRtTw.jpg",
            "https://s3.amazonaws.com/RudraCentre/ProductImages/Articles/Who-Is-Goddess-Durga-and-What-are-Her-Powers.jpg",
            "https://t4.ftcdn.net/jpg/07/17/43/21/360_F_717432140_M1seKMyGDiDm3oDPmj5Oym3Z3sNpEa1K.jpg"
            ]


        return JsonResponse({
            "reply": reply_text,
            "audio_url": audio_url,
            "story_images": story_images
        })

    return JsonResponse({"error": "POST required"})


def chat_page(request):
    return render(request, "chat.html")
