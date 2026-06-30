from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Nifty Sniper Live</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #f4f4f9; }
                h1 { color: #333; }
                p { color: #666; }
            </style>
        </head>
        <body>
            <h1>Welcome to Nifty Sniper Live! 🚀</h1>
            <p>Bhai, tera trading dashboard yahan banega.</p>
            <a href="/check_connection">Check Dhan API Connection</a>
        </body>
    </html>
    """

@app.get("/check_connection")
def check_connection():
    return {"status": "Success", "message": "Backend sahi chal raha hai!"}
