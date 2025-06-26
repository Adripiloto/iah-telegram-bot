import os
import json
import requests
from flask import Flask, request
import openai

# Configuración para OpenRouter
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/')
def home():
    return 'iah! está funcionando 🚀'

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    try:
        data = request.json
        print("\n📥 DATOS RECIBIDOS DE TELEGRAM:\n")
        print(json.dumps(data, indent=4))

        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user_message = message.get("text", "")

        print(f"\n✅ Mensaje: {user_message} | Chat ID: {chat_id}\n")

        # Llamada al modelo de OpenRouter (GPT-3.5 o el que elijas)
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # o prueba "mistralai/mixtral-8x7b"
            messages=[
                {
                    "role": "system",
                    "content": "Eres iah!, un asistente AI divertido, pícaro y cálido experto en amor y sexo."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response.choices[0].message.content.strip()

        payload = {
            "chat_id": chat_id,
            "text": reply
        }

        requests.post(TELEGRAM_API_URL, json=payload)

        return "OK", 200

    except Exception as e:
        print(f"\n❌ ERROR:\n\n{str(e)}\n")
        return "ERROR", 200


if __name__ == '__main__':
    app.run(debug=True)
