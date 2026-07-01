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
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
