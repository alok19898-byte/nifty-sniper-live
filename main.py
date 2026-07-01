from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. यह लाइन सबसे ज़रूरी है! यह सर्वर को static फोल्डर के बारे में बताती है
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. यह लाइन templates (HTML) फोल्डर के बारे में बताती है
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})r:</h2><p>{str(e)}</p>")
