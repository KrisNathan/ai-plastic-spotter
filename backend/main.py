import os
import shutil
import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from pathlib import Path
import tempfile
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
MODEL_PATH = Path("best.pt")
if not MODEL_PATH.exists():
    raise RuntimeError("Model file not found at backend/best.pt")

model = YOLO(MODEL_PATH)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        results = model(tmp_path, conf=0.1)
        
        result = results[0]
        
        plastic_count = len(result.boxes)
        
        im_bgr = cv2.imread(tmp_path)
        
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(im_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            cls = int(box.cls[0])
            label = result.names[cls]
            cv2.putText(im_bgr, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Encode image to base64
        _, buffer = cv2.imencode('.png', im_bgr)
        png_as_text = base64.b64encode(buffer).decode('utf-8')
        base64_image = f"data:image/png;base64,{png_as_text}"

        return {
            "count": plastic_count,
            "image": base64_image
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/")
def read_root():
    return {"message": "AI Plastic Spotter Backend is running"}
