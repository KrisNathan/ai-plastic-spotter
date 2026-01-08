# AI Plastic Spotter

A full-stack web application that uses AI to identify trash and provide recycling instructions.


## 📁 Project Structure

-   `backend/`: FastAPI application, YOLO inference.
-   `frontend/`: React application.
-   `train/`: Original model training notebooks and data (reference).

## 🌟 Features

-   **Instant Identification**: Uses a custom-trained YOLO11 model with SAHI (Slicing Aided Hyper Inference) to detect even small waste items with high accuracy.
-   **Modern UI**: Features a premium, dark-themed drag-and-drop interface built with React and Tailwind CSS v4.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python, Ultralytics YOLO11, SAHI
-   **Frontend**: React, TypeScript, Vite, Tailwind CSS
-   **Package Managers**: `uv` (Python), `npm` (Node.js)

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Node.js 18+

### 1. Backend Setup

Navigate to the backend directory and install dependencies using `uv`:

```bash
cd backend
# The dependencies will be automatically installed when you run the app
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

## Dataset

### BePLi Dataset v1: Beach Plastic Litter Dataset version 1

https://www.seanoe.org/data/00811/92297/

## References

[1]	M. Hidaka et al., ‘BePLi Dataset v1: Beach Plastic Litter Dataset version 1 for instance segmentation of beach plastic litter’, Data in Brief, vol. 48, p. 109176, 04 2023.
[2]	G. Jocher and J. Qiu, Ultralytics YOLO11. 2024.

```bib
@article{hidaka2023,
    author = {Hidaka, Mitsuko and Murakami, Koshiro and Koshidawa, Kenta and Kawahara, Shintaro and Sugiyama, Daisuke and Kako, Shin’ichiro and Matsuoka, Daisuke},
    year = {2023},
    month = {04},
    pages = {109176},
    title = {BePLi Dataset v1: Beach Plastic Litter Dataset version 1 for instance segmentation of beach plastic litter},
    volume = {48},
    journal = {Data in Brief},
    doi = {10.1016/j.dib.2023.109176}
}
@software{yolo11_ultralytics,
    author = {Glenn Jocher and Jing Qiu},
    title = {Ultralytics YOLO11},
    version = {11.0.0},
    year = {2024},
    url = {https://github.com/ultralytics/ultralytics},
    orcid = {0000-0001-5950-6979, 0000-0003-3783-7069},
    license = {AGPL-3.0}
}
```
