import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{BASE_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10
    )


@app.route("/")
def home():
    return "Forex Signal Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip().lower()

    if not chat_id:
        return {"ok": True}

    if text in ("/start", "/help"):
        send_message(
            chat_id,
            "Welcome to your Forex Signal Bot!\n\n"
            "Available commands:\n"
            "/start - Start the bot\n"
            "/status - Check bot status\n"
            "/signal - Check signal availability\n\n"
            "Live market scanning is not connected yet."
        )
    elif text == "/status":
        send_message(chat_id, "Telegram connection is working.")
    elif text == "/signal":
        send_message(
            chat_id,
            "Live signal detection is not connected yet. "
            "No trade recommendation is available."
        )
    else:
        send_message(chat_id, "Send /help to see available commands.")

    return {"ok": True}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
  )
