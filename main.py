from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. Static folder को लिंक करने की लाइन (CSS और JS के लिए)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Templates folder को सेट करना
templates = Jinja2Templates(directory="templates")

# 3. 🔥 CRITICAL FIX: Python 3.14 का बग फिक्स करने की जादुई लाइन 🔥
# यह लाइन Jinja2 के उस कैशे (Cache) सिस्टम को बंद कर देती है जो सर्वर को क्रैश कर रहा था।
templates.env.cache = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # FastAPI के लेटेस्ट वर्जन के हिसाब से एकदम सही तरीका
    return templates.TemplateResponse(request=request, name="index.html")
