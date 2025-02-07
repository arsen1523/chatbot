from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Загружаем API-ключ из .env файла
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с фронта

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Ошибка: пустое сообщение"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"Ошибка: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)