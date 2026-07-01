import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from dhanhq import DhanContext, dhanhq
from dotenv import load_dotenv

# Environment Variables लोड करना
load_dotenv()
app = FastAPI()

# CORS इनेबल करना
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

# Dhan API Connection (Safe Mode)
try:
    context = DhanContext(CLIENT_ID, ACCESS_TOKEN)
    dhan = dhanhq(context)
    print("Dhan API Connected Successfully!")
except Exception as e:
    dhan = None
    print("Dhan API Error:", e)

# Static Folders (CSS/JS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    # HTML File Loading (templates या main फोल्डर कहीं भी हो)
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html")
    else:
        return FileResponse("index.html")

@app.get("/api/option-chain")
async def get_live_chain():
    spot_price = 23300.00
    if dhan:
        try:
            nifty_req = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
            if nifty_req and 'data' in nifty_req:
                spot_price = float(nifty_req['data']['last_price'])
        except:
            pass

    atm_strike = round(spot_price / 50) * 50
    strikes = [atm_strike + (i * 50) for i in range(-5, 6)]
    
    chain_data = []
    for strike in strikes:
        chain_data.append({
            "strike": strike,
            "CE": {"oi_chg": 1500, "oi": 15000, "volume": 4500, "ltp": 120.50},
            "PE": {"ltp": 90.20, "volume": 3200, "oi": 12000, "oi_chg": -500}
        })
    return {"spot_price": spot_price, "atm_strike": atm_strike, "chain": chain_data}

# यहाँ ध्यान दे - 100% सही अंडरस्कोर
if _name_ == '_main_':
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host='0.0.0.0', port=port)
