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

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# क्रेडेंशियल्स - बस ये दो ही वेरिएबल लेने हैं
CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

# Dhan Initialization - यहाँ पक्का ध्यान रख, सिर्फ 2 ही चीज़ें पास हो रही हैं
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
        # Option Chain Data fetch करना
        # आज 01-07-2026 है, तो एक्सपायरी डेट उसी हिसाब से रखें
        data = dhan.get_option_chain(
            underlying_security_id="26000",
            underlying_type="INDEX",
            expiry_date="2026-07-02"
        )
        return {"spot_price": "Live", "data": data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
  
