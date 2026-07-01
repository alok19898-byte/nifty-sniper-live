import os
import uvicorn
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from dhanhq import dhanhq  # यह लाइन जरूरी है क्योंकि तुम इसे इस्तेमाल कर रहे हो

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

CLIENT_ID = os.environ.get('DHAN_CLIENT_ID')
ACCESS_TOKEN = os.environ.get('DHAN_ACCESS_TOKEN')

# API का सही इस्तेमाल
@app.get("/api/expiry-list")
async def get_expiry():
    url = "https://api.dhan.co/v2/optionchain/expirylist"
    headers = {
        "Content-Type": "application/json",
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID
    }
    payload = {
        "UnderlyingScrip": 13,
        "UnderlyingSeg": "IDX_I"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
