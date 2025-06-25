import os
import openai
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return "iah! is running"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    message = data.get('message', {}).get('text')
    chat_id = data.get('message', {}).get('chat', {}).get('id')

    if message:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cambia por gpt-4 si tu API lo permite
            messages=[
                {"role": "system", "content": "Eres iah!, un asistente AI divertido, sexy y cariñoso. Aconsejas, entretienes y respondes con picardía y humor dependiendo de la persona que escribe."},
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content']

        send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(send_url, json={
            "chat_id": chat_id,
            "text": reply
        })

    return "ok"
