import os
import shutil
import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
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
MODEL_PATH = Path("bester.pt")
if not MODEL_PATH.exists():
    raise RuntimeError("Model file not found at backend/bester.pt")

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolo11', 
    model_path=str(MODEL_PATH),
    confidence_threshold=0.6, 
    device="cuda"  
)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # save uploaded file 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # sliced Prediction
        result = get_sliced_prediction(
            tmp_path,
            detection_model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2
        )
        
        plastic_count = len(result.object_prediction_list)
        
        # save 
        # export the visualization to a real file first.
        # use temp dir for output to avoid cluttering main folder
        with tempfile.TemporaryDirectory() as output_dir:
            stem = Path(tmp_path).stem
            result.export_visuals(export_dir=output_dir, file_name=stem)
            
            saved_file_path = os.path.join(output_dir, stem + ".png")
            
            if os.path.exists(saved_file_path):
                 with open(saved_file_path, "rb") as image_file:
                    png_as_text = base64.b64encode(image_file.read()).decode('utf-8')
                    base64_image = f"data:image/png;base64,{png_as_text}"
            else:
                 with open(tmp_path, "rb") as image_file:
                     im_bgr = cv2.imread(tmp_path)
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
