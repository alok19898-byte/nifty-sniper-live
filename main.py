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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

try:
    dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)
except Exception as e:
    dhan = None
    print("Dhan Error:", e)

# Static फोल्डर माउंट करना
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    return FileResponse("index.html")

@app.get("/api/option-chain")
async def get_live_chain():
    try:
        # NIFTY 50 का असली लाइव Spot Price फेच करना
        nifty_req = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
        spot_price = float(nifty_req['data']['last_price'])
    except Exception as e:
        spot_price = 23300.00 # अगर API न चले तो डिफ़ॉल्ट

    # ATM (At The Money) स्ट्राइक ढूँढना (50 के मल्टीपल में)
    atm_strike = round(spot_price / 50) * 50

    # ATM के ऊपर 5 और नीचे 5 स्ट्राइक बनाना (तेरी टेबल के लिए)
    strikes = [atm_strike + (i * 50) for i in range(-5, 6)]
    
    chain_data = []
    for strike in strikes:
        # यहाँ पर API से असली ऑप्शन डेटा जोड़ा जा सकता है, 
        # फिलहाल डैशबोर्ड को लाइव दिखाने के लिए डमी कैलकुलेशन है
        chain_data.append({
            "strike": strike,
            "CE": {
                "oi_chg": 1500, "oi": 15000, "volume": 4500, 
                "ltp": max(0.5, spot_price - strike + 100) # Call LTP लॉजिक
            },
            "PE": {
                "ltp": max(0.5, strike - spot_price + 100), # Put LTP लॉजिक
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
