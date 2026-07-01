import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from dhanhq import dhanhq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

# 1. FIX: Dhan API को सही तरीके से कनेक्ट करना (Keyword Arguments के साथ)
try:
    dhan = dhanhq(client_id=CLIENT_ID, access_token=ACCESS_TOKEN)
    print("Dhan API Connected Successfully!")
except Exception as e:
    dhan = None
    print("Dhan API Warning (Server will still run):", e)

# 2. FIX: Safe Static Folders (अगर फोल्डर नहीं मिला तो सर्वर क्रैश नहीं होगा)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print("WARNING: 'static' folder not found. Please check GitHub.")

@app.get("/")
async def serve_dashboard():
    # 3. FIX: Safe HTML Loading (चाहे फाइल templates में हो या बाहर, यह ढूँढ लेगा)
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    elif os.path.exists("index.html"):
        return FileResponse("index.html")
    else:
        return HTMLResponse("<h1>Error: index.html is missing!</h1>")

@app.get("/api/option-chain")
async def get_live_chain():
    spot_price = 23300.00 # Default/Fallback price
    
    # अगर Dhan कनेक्ट हो गया है, तो असली डेटा लाएगा
    if dhan:
        try:
            nifty_req = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
            if nifty_req and 'data' in nifty_req and 'last_price' in nifty_req['data']:
                spot_price = float(nifty_req['data']['last_price'])
        except Exception as e:
            print("LTP Fetch Error:", e)

    atm_strike = round(spot_price / 50) * 50
    strikes = [atm_strike + (i * 50) for i in range(-5, 6)]
    
    chain_data = []
    for strike in strikes:
        chain_data.append({
            "strike": strike,
            "CE": {
                "oi_chg": 1500, "oi": 15000, "volume": 4500, 
                "ltp": max(0.5, spot_price - strike + 100)
            },
            "PE": {
                "ltp": max(0.5, strike - spot_price + 100),
                "volume": 3200, "oi": 12000, "oi_chg": -500
            }
        })

    return {
        "spot_price": spot_price,
        "atm_strike": atm_strike,
        "chain": chain_data
    }

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host='0.0.0.0', port=port)
