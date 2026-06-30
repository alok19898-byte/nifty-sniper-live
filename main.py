from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import secrets

app = FastAPI()
security = HTTPBasic()

# तुम्हारा अपडेटेड क्रेडेंशियल्स
MY_USER = "aalokraj"
MY_PASS = "Aalokraj@123"

def verify_login(credentials: HTTPBasicCredentials = Depends(security)):
    # यहाँ यूजरनेम और पासवर्ड की जांच हो रही है
    if credentials.username == MY_USER and credentials.password == MY_PASS:
        return credentials.username
    
    # गलत होने पर ये एरर आएगा
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="गलत यूजरनेम या पासवर्ड!",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.get("/", dependencies=[Depends(verify_login)])
async def get_dashboard():
    # यह तुम्हारी index.html को लोड करेगा
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return {"error": "index.html फाइल नहीं मिली!"}
