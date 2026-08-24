import io
import time
import requests
from PIL import Image, ImageDraw

base_url = "http://127.0.0.1:8000"

print("Waiting for server to start...")
time.sleep(2)

# 1. Test /health
print("\n--- Testing GET /health ---")
try:
    resp = requests.get(f"{base_url}/health")
    print("Health response code:", resp.status_code)
    print("Health response body:", resp.json())
except Exception as e:
    print("Health check failed:", e)

# 2. Test /docs
print("\n--- Testing GET /docs ---")
try:
    resp = requests.get(f"{base_url}/docs")
    print("Docs response code:", resp.status_code)
    print("Docs reachable:", resp.status_code == 200)
except Exception as e:
    print("Docs check failed:", e)

# 3. Test /predict
print("\n--- Testing POST /predict ---")
try:
    # Create a synthetic crop leaf image for testing
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 50, 170, 170), fill=(139, 69, 19))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    files = {"file": ("test_leaf.jpg", img_bytes, "image/jpeg")}
    resp = requests.post(f"{base_url}/predict", files=files)
    print("Predict response code:", resp.status_code)
    res_json = resp.json()
    print("Predict response body:")
    print(res_json)
    
    if res_json.get("success"):
        print("\nSUCCESS: Prediction verified!")
        print("Predicted Class:", res_json.get("predicted_class"))
        print("Confidence:", res_json.get("confidence"))
        print("Top Predictions:", res_json.get("top_predictions"))
except Exception as e:
    print("Predict test failed:", e)
