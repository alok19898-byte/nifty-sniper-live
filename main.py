from fastapi import FastAPI
from dhanhq import dhanhq
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

# Dhan API कनेक्शन
dhan = dhanhq(client_id, access_token)

app = FastAPI()

# जिन इंडेक्स का डेटा हमें चाहिए
symbols_list = ["NIFTY 50", "NIFTY BANK", "NIFTY FIN SERVICE"]

@app.get("/")
def read_root():
    return {"message": "Bhai tera FastAPI Backend start ho gaya hai!"}

@app.get("/check_connection")
def check_connection():
    try:
        # फंड चेक करके कनेक्शन टेस्ट कर रहे हैं
        fund_limit = dhan.get_fund_limits()
        return {"status": "Success", "message": "Dhan API mast connect ho gayi!", "data": fund_limit}
    except Exception as e:
        return {"status": "Error", "message": str(e)}