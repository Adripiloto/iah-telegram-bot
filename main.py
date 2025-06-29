from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configura tus tokens como variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def home():
    return 'Bot IA 🤖 está vivo'

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    print("📥 DATOS RECIBIDOS DE TELEGRAM:\n", data)

    try:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # Mensaje para enviar a OpenRouter (GPT-3.5 Turbo)
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "Eres un asistente amistoso y útil."},
                {"role": "user", "content": user_message}
            ]
        }

        print("📡 Enviando mensaje a OpenRouter...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)

        result = response.json()
        print("✅ RESPUESTA DE OPENROUTER:\n", result)

        ai_reply = result["choices"][0]["message"]["content"]

        # Enviar mensaje a Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        message_data = {
            "chat_id": chat_id,
            "text": ai_reply
        }
        telegram_response = requests.post(telegram_url, json=message_data)
        print("✅ RESPUESTA ENVIADA A TELEGRAM")

    except Exception as e:
        print("❌ ERROR en el webhook:", e)

    return "OK", 200
