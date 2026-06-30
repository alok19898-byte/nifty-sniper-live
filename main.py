from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
security = HTTPBasic()

MY_USER = "aalokraj"
MY_PASS = "Aalokraj@123"

def verify_login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == MY_USER and credentials.password == MY_PASS:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.get("/", dependencies=[Depends(verify_login)])
async def get_dashboard():
    try:
        # Check 1: क्या फाइल templates फोल्डर में है?
        if os.path.exists("templates/index.html"):
            with open("templates/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        
        # Check 2: क्या फाइल बाहर (main root) पड़ी है?
        elif os.path.exists("index.html"):
            with open("index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        
        # Check 3: अगर फाइल मिले ही ना, तो स्क्रीन पर बताएगा कि कौन-कौन सी फाइलें मौजूद हैं
        else:
            current_files = os.listdir('.')
            return HTMLResponse(content=f"<h3>Error: index.html mili hi nahi!</h3><p>Server par abhi ye files/folders hain: {current_files}</p>")
            
    except Exception as e:
        # अगर कोई और पाइथन एरर हुआ, तो वो भी स्क्रीन पर छप जाएगा
        return HTMLResponse(content=f"<h2>System Error:</h2><p>{str(e)}</p>")
