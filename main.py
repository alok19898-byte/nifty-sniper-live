import os
from fastapi.responses import HTMLResponse

@app.get("/", dependencies=[Depends(verify_login)])
async def get_dashboard():
    # यह कोड 'templates' फोल्डर के अंदर index.html को ढूंढेगा
    file_path = os.path.join("templates", "index.html")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return {"error": f"templates folder me file nahi mili! Check karo. Error: {e}"}
