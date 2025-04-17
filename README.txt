📦 LINE Bot Notify Flask 範例

✅ 功能：
- /callback：接收 LINE 使用者訊息，自動回應
- /notify：從 Python 外部 POST 通知訊息到你 LINE
- / ：首頁測試連線

🚀 使用方法：
1. pip install -r requirements.txt
2. 複製 `.env.example` → `.env` 並填入你的 Token/Secret
3. python app.py
4. 用 ngrok 開啟：ngrok http 5000
5. 把 ngrok 給的網址 + `/callback` 填入 LINE Webhook URL 並啟用
6. 在 LINE 傳訊息給 Bot 測試！

📤 傳訊息給自己：
curl -X POST http://localhost:5000/notify -H "Content-Type: application/json" -d '{"to": "你的用戶ID", "message": "Hello from Python!"}'
