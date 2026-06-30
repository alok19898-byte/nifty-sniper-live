import random
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # निफ्टी का रैंडम भाव जनरेट हो रहा है
    random_price = round(random.uniform(23000, 24000), 2)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "price": random_price,
            "status": "Live & Running"
        }
    )
