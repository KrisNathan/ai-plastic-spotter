import requests
from pathlib import Path

url = "http://127.0.0.1:8000/analyze"
image_path = Path("../ai-plastic-spotter/plastic-bottle-waste.png")

if not image_path.exists():
    print(f"Error: Image not found at {image_path}")
    exit(1)

files = {"file": open(image_path, "rb")}
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Request failed: {e}")
