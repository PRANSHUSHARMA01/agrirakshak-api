import os
import json
import traceback

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np

output = []

def log(msg):
    output.append(str(msg))
    print(msg)

log("--- TEST MODEL SCRIPT ---")
model_path = "best_agri_finetuned.keras"
class_path = "class_names.json"

try:
    log("Loading Keras model...")
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception:
        log("Loading with compile=False...")
        model = tf.keras.models.load_model(model_path, compile=False)
        
    log("MODEL LOADED SUCCESSFULLY")
    log(f"INPUT SHAPE: {model.input_shape}")
    log(f"OUTPUT SHAPE: {model.output_shape}")

    # Test inference
    dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
    preds = model.predict(dummy, verbose=0)
    log(f"Inference output shape: {preds.shape}")
    log(f"Top prediction index: {np.argmax(preds[0])}")

except Exception as e:
    log(f"MODEL LOADING FAILED: {e}")
    log(traceback.format_exc())

try:
    with open(class_path, "r", encoding="utf-8") as f:
        classes = json.load(f)
    log(f"CLASS COUNT: {len(classes)}")
    log(f"Unique classes: {len(set(classes))}")
except Exception as e:
    log(f"CLASS NAMES LOADING FAILED: {e}")

with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
