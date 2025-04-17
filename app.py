import os
import openai
import json
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 讀取 .env 檔
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
USER_ID = os.getenv("USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

openai.api_key = OPENAI_API_KEY

# 預設模式
current_mode = {"type": "standard"}  # standard, academic, roleplay
roleplay_instruction = "你是一個溫柔體貼的星座導師"

app = Flask(__name__)

@app.route("/")
def hello():
    return "LINE Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id
    print("\u6536\u5230\u8a0a\u606f:", user_message)

    if user_message.startswith("/\u6a21\u5f0f"):
        mode = user_message.replace("/\u6a21\u5f0f", "").strip()
        if mode in ["\u6a19\u6e96", "\u5b78\u8853", "\u89d2\u8272"]:
            current_mode["type"] = {
                "\u6a19\u6e96": "standard",
                "\u5b78\u8853": "academic",
                "\u89d2\u8272": "roleplay"
            }[mode]
            reply = f"\u6a21\u5f0f\u5df2\u5207\u63db\u70ba {mode}"
        else:
            reply = "\u8acb\u6307\u5b9a\u6b63\u78ba\u6a21\u5f0f: /\u6a21\u5f0f [\u6a19\u6e96|學\u8853|\u89d2\u8272]"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    # ===準備 messages===
    if current_mode["type"] == "standard":
        messages = [
            {"role": "user", "content": user_message}
        ]
    elif current_mode["type"] == "academic":
        messages = [
            {"role": "system", "content": "你是一位精通學術、指出證據、嚴詳說明的學者"},
            {"role": "user", "content": user_message}
        ]
    else:  # roleplay
        messages = [
            {"role": "system", "content": roleplay_instruction},
            {"role": "user", "content": user_message}
        ]

    # ===取 GPT-4o 答案===
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"[ERROR]\n{str(e)}"

    # === 回覆給用戶 ===
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)