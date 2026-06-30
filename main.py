mport random
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # यहाँ हम रैंडम निफ्टी भाव जनरेट कर रहे हैं
    random_price = round(random.uniform(23000, 24000), 2)
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "price": random_price,
            "status": "Live & Running"
        }
    )
