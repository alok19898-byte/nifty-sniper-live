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

# Dhan API Connection
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

@app.get("/api/option-chain")
async def get_live_chain():
    if not dhan:
        return {"error": "Dhan API not connected"}
    
    try:
        # यहाँ हम try-except लगा रहे हैं ताकि अगर एक कमांड काम न करे तो दूसरा चल जाए
        try:
            # कोशिश करते हैं पहले नए तरीके से
            ltp_data = dhan.ltp(exchange_segment='NSE_EQ', security_id='26000')
            spot_price = float(ltp_data[0]['ltp'])
        except:
            # अगर नया काम न करे, तो पुराने तरीके से ट्राई करते हैं
            ltp_data = dhan.get_ltp_data(exchange_segment='NSE_EQ', security_id='26000')
            spot_price = float(ltp_data['data']['last_price'])
            
        return {
            "spot_price": spot_price,
            "data": [] 
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
