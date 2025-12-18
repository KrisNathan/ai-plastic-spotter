## Dataset

Stored using git-lfs

### BePLi Dataset v1: Beach Plastic Litter Dataset version 1

https://www.seanoe.org/data/00811/92297/

Mitsuko Hidaka, Koshiro Murakami, Kenta Koshidawa, Shintaro Kawahara, Daisuke Sugiyama, Shin’ichiro Kako, Daisuke Matsuoka (2023). BePLi Dataset v1: Beach Plastic Litter Dataset version 1. SEANOE. https://doi.org/10.17882/92297

### RealWaste

https://archive.ics.uci.edu/static/public/908/realwaste.zip

S. Single, S. Iranmanesh, and R. Raad. "RealWaste," UCI Machine Learning Repository, 2023. [Online]. Available: https://doi.org/10.24432/C5SS4G.

The dataset is composed of the following labels and image counts:

- Cardboard: 461
- Food Organics: 411
- Glass: 420
- Metal: 790
- Miscellaneous Trash: 495
- Paper: 500
- Plastic: 921
- Textile Trash: 318
- Vegetation: 436



# AI Plastic Spotter

A full-stack web application that uses AI to identify trash and provide recycling instructions.

## 🌟 Features

-   **Instant Identification**: Uses a custom-trained YOLOv8 model to classify waste into categories (Plastic, Glass, Metal, etc.).
-   **Smart Recycling Advice**: Integrates with Google's Gemini 2.5 Flash Lite to generate specific disposal instructions and interesting facts.
-   **Modern UI**: Features a premium, dark-themed drag-and-drop interface built with React and Tailwind CSS v4.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python, Ultralytics YOLO, Google Generative AI
-   **Frontend**: React, TypeScript, Vite, Tailwind CSS
-   **Package Managers**: `uv` (Python), `npm` (Node.js)

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Node.js 18+
-   A Google Gemini API Key

### 1. Backend Setup

Navigate to the backend directory and install dependencies using `uv`:

```bash
cd backend
# The dependencies will be automatically installed when you run the app
```

Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Start the backend server:

```bash
uv run python -m uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 2. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

Open your browser to `http://localhost:5173` to use the app!

## 📁 Project Structure

-   `backend/`: FastAPI application, YOLO model (`model.pt`), and logic.
-   `frontend/`: React application with Tailwind styling.
-   `ai-plastic-spotter/`: Original model training notebooks and data (reference).
