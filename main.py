from fastapi import FastAPI
import os
from dotenv import load_dotenv

# load_dotenv() # अभी के लिए कमेंट कर दिया है क्योंकि Render में हम सीधे Variable डालेंगे
# client_id = os.getenv("CLIENT_ID")
# access_token = os.getenv("ACCESS_TOKEN")

# Dhan API कनेक्शन - अभी इसे कमेंट रखा है ताकि सर्वर क्रैश न हो
# from dhanhq import dhanhq
# dhan = dhanhq(client_id, access_token)

app = FastAPI()

# बेसिक रूट टेस्ट करने के लिए
@app.get("/")
def read_root():
    return {"message": "Bhai tera FastAPI Backend start ho gaya hai!"}

# कनेक्शन चेक करने वाला रूट
@app.get("/check_connection")
def check_connection():
    try:
        # यहाँ जब API कीज़ डालोगे, तब इसे अन-कमेंट कर देना
        # fund_limit = dhan.get_fund_limits()
        # return {"status": "Success", "data": fund_limit}
        
        return {"status": "Success", "message": "Backend sahi chal raha hai, abhi API connect nahi hai!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
