from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

# अपना यूजरनेम और पासवर्ड यहाँ सेट करें
USERNAME = "admin"
PASSWORD = "password123" 

def verify_login(credentials: HTTPBasicCredentials = Depends(security)):
    # पासवर्ड चेक करने का तरीका
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="गलत पासवर्ड! वापस कोशिश करें.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# अब किसी भी राउट के आगे 'dependencies=[Depends(verify_login)]' जोड़ दें
@app.get("/", dependencies=[Depends(verify_login)])
async def get_dashboard():
    # आपकी वेबसाइट का बाकी कोड यहाँ आएगा
    return {"message": "पासवर्ड सही है, डैशबोर्ड में आपका स्वागत है!"}
