import os
import openai
from flask import Flask, request
import requests

app = Flask(__name__)

# Carga de variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Configura la clave de OpenAI
openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return "iah! is running"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    try:
        data = request.get_json()
        print("📥 DATOS RECIBIDOS DE TELEGRAM:")
        print(data)

        message = data.get('message', {}).get('text')
        chat_id = data.get('message', {}).get('chat', {}).get('id')

        if message and chat_id:
            print(f"✅ Mensaje: {message} | Chat ID: {chat_id}")

            # Llamada a OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Cambia a "gpt-4" si tienes acceso
                messages=[
                    {
                        "role": "system",
                        "content": "Eres iah!, un asistente AI divertido, sexy y cariñoso. Aconsejas, entretienes y respondes con picardía y humor dependiendo de la persona que escribe."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )

            reply = response['choices'][0]['message']['content']
            print("💬 Respuesta generada:", reply)

            # Envío de respuesta a Telegram
            send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            telegram_response = requests.post(send_url, json={
                "chat_id": chat_id,
                "text": reply
            })

            print("📤 Resultado de enviar mensaje:", telegram_response.status_code, telegram_response.text)

        else:
            print("⚠️ No se encontró texto o chat_id en el mensaje recibido.")

    except Exception as e:
        print("❌ ERROR al procesar el mensaje:", str(e))

    return "ok"
