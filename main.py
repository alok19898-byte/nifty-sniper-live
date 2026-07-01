import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dhanhq import dhanhq
from dotenv import load_dotenv

# .env लोड करना (Render के Environment Variables यहाँ से मिल जाएंगे)
load_dotenv()

app = FastAPI()

# CORS इनेबल करना ताकि फ्रंटएंड डेटा ले सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables से कीज़ उठाना
CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')
API_KEY = os.environ.get('DHAN_API_KEY')

# DhanHQ का क्लाइंट
dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

@app.get('/get-data')
async def get_nifty_data():
    try:
        # Nifty 50 LTP
        data = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
        return data
    except Exception as e:
        return {"error": str(e)}

if _name_ == '_main_':
    # Render के लिए पोर्ट 10000 फिक्स रखना
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host='0.0.0.0', port=port)
