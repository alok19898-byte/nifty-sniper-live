from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dhanhq import dhanhq
import os

app = FastAPI()

# Frontend से कनेक्शन के लिए CORS इनेबल करना
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables से कीज़ उठाना
CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

@app.get('/get-data')
async def get_nifty_data():
    try:
        # Nifty 50 का LTP डेटा
        data = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
        return data
    except Exception as e:
        return {"error": str(e)}

# Render के लिए पोर्ट सेट करना
if _name_ == '_main_':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=10000)
