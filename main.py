import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dhanhq import dhanhq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=[""], allow_methods=[""], allow_headers=["*"])

# क्रेडेंशियल्स एन्वायरमेंट वेरिएबल्स से लें
CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

# Dhan ऑब्जेक्ट को इनिशियलाइज करें
dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    return FileResponse("index.html")

@app.get("/api/option-chain")
async def get_live_chain():
    try:
        # लेटेस्ट लाइव ऑप्शन चेन डेटा प्राप्त करें
        # सिक्योरिटी आईडी 26000 (Nifty) और आज की या आने वाली एक्सपायरी डेट डालें
        data = dhan.get_option_chain(
            underlying_security_id="26000",
            underlying_type="INDEX",
            expiry_date="2026-07-02" # इसे अपने हिसाब से अपडेट करते रहना भाई
        )
        
        # चूँकि हमें स्पॉट प्राइस भी चाहिए, हम इसे यहाँ से निकाल सकते हैं
        # या अलग से LTP कॉल कर सकते हैं
        return {
            "spot_price": "Live", 
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
