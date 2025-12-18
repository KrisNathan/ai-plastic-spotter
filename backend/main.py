import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import google.generativeai as genai
from pathlib import Path
import tempfile
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
MODEL_PATH = Path("model.pt")
if not MODEL_PATH.exists():
    raise RuntimeError("Model file not found at backend/model.pt")

model = YOLO(MODEL_PATH)

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not set. Gemini features will fail.")

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # 1. Run YOLO Inference
        results = model(tmp_path)
        
        # Get the top prediction
        probs = results[0].probs
        top1_index = probs.top1
        predicted_class = results[0].names[top1_index]
        confidence = probs.top1conf.item()

        print(f"Detected: {predicted_class} ({confidence:.2f})")

        # 2. Call Gemini API
        gemini_response = {"description": "Gemini API Key missing", "action": "N/A"}
        
        if GEMINI_API_KEY:
            try:
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                    "response_mime_type": "application/json",
                }
                model_gemini = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    generation_config=generation_config,
                )
                
                prompt = f"""
                I have identified a piece of trash as '{predicted_class}'.
                Please provide a structured JSON response with two fields:
                1. "description": A brief, interesting fact about this type of waste (max 2 sentences).
                2. "action": Specific instructions on how to properly dispose of or recycle this category of waste.
                
                Output JSON only.
                """
                
                response = model_gemini.generate_content(prompt)
                gemini_response = response.text
                # Clean up json string if needed (sometimes it includes ```json ... ```)
                if gemini_response.startswith("```json"):
                    gemini_response = gemini_response[7:-3]
                
                import json
                gemini_response = json.loads(gemini_response)

            except Exception as e:
                print(f"Gemini Error: {e}")
                # Return a cleaner error for the UI
                gemini_response = {
                    "description": "Could not retrieve info from Gemini (Rate Limit or Model Error).",
                    "action": "Please try again in a few moments."
                }

        return {
            "label": predicted_class,
            "confidence": confidence,
            "gemini": gemini_response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/")
def read_root():
    return {"message": "AI Plastic Spotter Backend is running"}
