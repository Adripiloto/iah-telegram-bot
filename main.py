import os
import json
import requests
from flask import Flask, request
import openai

app = Flask(__name__)

# Configura OpenRouter
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1"

@app.route("/")
def home():
    return "Bot IA 🤖 está vivo"

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    print("📥 DATOS RECIBIDOS DE TELEGRAM:")
    print(json.dumps(data, indent=4))

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        try:
            # ✅ Llama a OpenRouter con la nueva forma
            response = openai.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
            )

            ai_response = response.choices[0].message.content.strip()

            # ✅ Envía la respuesta al usuario en Telegram
            send_telegram_message(chat_id, ai_response)

        except Exception as e:
            print("❌ ERROR:")
            print(e)
            send_telegram_message(chat_id, "⚠️ Error: no he podido responder.")

    return "OK"

def send_telegram_message(chat_id, text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
