# AgriRakshak AI API Backend

Production-ready FastAPI backend for AgriRakshak crop disease detection system using TensorFlow / Keras deep learning model.

## Required Model Files

Before running the API, place the following two files (downloaded from your Kaggle notebook output) into the root folder of this project (`c:\Users\prans\OneDrive\Desktop\agrirakshak-api`):

1. **`best_agri_finetuned.keras`**: Trained Keras fine-tuned crop disease model (Input shape: `(None, 224, 224, 3)`, Output shape: `(None, 32)`).
2. **`class_names.json`**: JSON array containing the 32 crop disease class labels.

---

## Setup & Running Guide

### 1. Activate the Virtual Environment (`venv`)

#### Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt (cmd):
```cmd
.\venv\Scripts\activate.bat
```

#### Git Bash / Linux / macOS:
```bash
source venv/Scripts/activate
```

---

### 2. Install Dependencies

Install the required Python 3.11 compatible dependencies:
```bash
pip install -r requirements.txt
```

---

### 3. Start the FastAPI Server

To start the API local development server:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

### 4. Interactive API Documentation (Swagger Docs)

Once the server is running, open your web browser and navigate to:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### 5. Testing API Endpoints

#### Root Endpoint (`GET /`)
```bash
curl http://127.0.0.1:8000/
```
**Response:**
```json
{
  "name": "AgriRakshak AI API",
  "version": "1.0.0",
  "status": "online"
}
```

#### Health Check (`GET /health`)
```bash
curl http://127.0.0.1:8000/health
```
**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes": 32
}
```

#### Disease Prediction (`POST /predict`)

Upload an image file using `multipart/form-data`:

##### Using cURL:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/crop_leaf.jpg"
```

##### Using Python `requests`:
```python
import requests

url = "http://127.0.0.1:8000/predict"
with open("crop_leaf.jpg", "rb") as f:
    files = {"file": ("crop_leaf.jpg", f, "image/jpeg")}
    response = requests.post(url, files=files)
    print(response.json())
```

**Successful Response Example:**
```json
{
  "success": true,
  "prediction": "Tomato___Bacterial_spot",
  "confidence": 98.45,
  "class_index": 12
}
```
