from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import base64, io, pathlib, threading, time, webbrowser
from pipeline import get_amount

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def open_browser():
    time.sleep(1) 
    file_path = pathlib.Path("C:/Users/evech/OneDrive/Documents/GitHub/ppp-2025/Exercises/Hanna-und-Eve/index.html").resolve()
    webbrowser.open(f"{file_path.as_posix()}")

@app.post("/website")
async def website(request: Request):
    data = await request.json()
    image_data = data["image"]
    header, encoded = image_data.split(",", 1)

    img_bytes = base64.b64decode(encoded)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    result = get_amount(img)

    return JSONResponse(content={"message": result})

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=False)
