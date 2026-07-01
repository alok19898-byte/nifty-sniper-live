import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dhanhq import DhanContext, dhanhq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=[""], allow_methods=[""], allow_headers=["*"])

CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

try:
    context = DhanContext(CLIENT_ID, ACCESS_TOKEN)
    dhan = dhanhq(context)
except Exception:
    dhan = None

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    return FileResponse("index.html")

# यह रहा असली डेटा फेच करने वाला हिस्सा
@app.get("/api/option-chain")
async def get_live_chain():
    try:
        # NIFTY 50 का स्पॉट प्राइस फेच करना
        ltp_data = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
        spot = float(ltp_data['data']['last_price'])
        
        # यहाँ हम ऑप्शन चेन का डेटा लेंगे
        # ध्यान दें: dhanhq में ऑप्शन चेन के लिए सही symbol और exchange_segment ज़रूरी है
        chain = dhan.get_option_chain_data(symbol='NIFTY', exchange_segment='NSE_FNO')
        
        return {
            "spot_price": spot,
            "data": chain
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
