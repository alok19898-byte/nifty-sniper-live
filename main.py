from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import secrets
import os

app = FastAPI()
security = HTTPBasic()

# तुम्हारा लॉगिन
MY_USER = "aalokraj"
MY_PASS = "Aalokraj@123"

def verify_login(credentials: HTTPBasicCredentials = Depends(security)):
    if secrets.compare_digest(credentials.username, MY_USER) and secrets.compare_digest(credentials.password, MY_PASS):
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="गलत पासवर्ड!",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.get("/", dependencies=[Depends(verify_login)])
async def get_dashboard():
    # ब्रह्मास्त्र: Absolute Path (यह main.py जहाँ है, उसी की लोकेशन निकालेगा)
    BASE_DIR = os.path.dirname(os.path.abspath(_file_))
    file_path = os.path.join(BASE_DIR, "templates", "index.html")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        # अगर फिर भी नहीं मिली, तो यह स्क्रीन पर पूरा 'Path' दिखा देगा कि वो कहाँ ढूंढ रहा है
        error_msg = f"<h3>File abhi bhi nahi mili!</h3><p>Server yahan dhundh raha hai: <b>{file_path}</b></p><p>Error: {e}</p>"
        return HTMLResponse(content=error_msg)
