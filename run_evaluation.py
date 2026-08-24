import os
import json
import zipfile
import io
import time
import requests
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import keras
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# ============================================================
# SETUP & LOADING RESOURCES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_agri_finetuned.keras"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"
EVAL_DIR = BASE_DIR / "evaluation"
EVAL_DIR.mkdir(exist_ok=True)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

class_to_idx = {name: idx for idx, name in enumerate(class_names)}
num_classes = len(class_names)

print(f"Loaded {num_classes} class names.")
print(f"Loading model from {MODEL_PATH}...")
model = keras.models.load_model(str(MODEL_PATH))
print(f"Model input shape: {model.input_shape}")
print(f"Model output shape: {model.output_shape}")

# ============================================================
# COLLECT TEST IMAGES FROM DATASETS
# ============================================================

images_list = []
labels_list = []
paths_list = []
dataset_names_list = []

# 1. Rice and Maize Dataset
rm_root = Path(r"C:\Users\prans\Downloads\Rice_and_Maize_Dataset")
if rm_root.exists():
    for root, dirs, files in os.walk(rm_root):
        folder_name = os.path.basename(root)
        target_class = None
        if folder_name in class_to_idx:
            target_class = folder_name
        elif folder_name == "Healthy":
            parent = os.path.basename(os.path.dirname(root))
            if parent == "Rice":
                target_class = "Rice_Healthy"
            elif parent == "Maize":
                target_class = "Maize_Healthy"
        
        if target_class and target_class in class_to_idx:
            c_idx = class_to_idx[target_class]
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    fpath = os.path.join(root, file)
                    try:
                        img = Image.open(fpath).convert("RGB").resize((224, 224))
                        images_list.append(np.array(img, dtype=np.float32))
                        labels_list.append(c_idx)
                        paths_list.append(fpath)
                        dataset_names_list.append("Rice_and_Maize_Dataset")
                    except Exception as e:
                        print(f"Failed to read {fpath}: {e}")

# 2. PlantDoc Zip Dataset (for Pepper, Potato, Tomato classes)
plantdoc_zip_path = Path(r"C:\Users\prans\Downloads\PlantDoc-Dataset-master.zip")
if plantdoc_zip_path.exists():
    mapping = {
        "test/Bell_pepper leaf spot/": "Pepper__bell___Bacterial_spot",
        "test/Bell_pepper leaf/": "Pepper__bell___healthy",
        "test/Potato leaf early blight/": "Potato___Early_blight",
        "test/Potato leaf late blight/": "Potato___Late_blight",
        "test/Tomato leaf bacterial spot/": "Tomato_Bacterial_spot",
        "test/Tomato Early blight leaf/": "Tomato_Early_blight",
        "test/Tomato leaf late blight/": "Tomato_Late_blight",
        "test/Tomato mold leaf/": "Tomato_Leaf_Mold",
        "test/Tomato Septoria leaf spot/": "Tomato_Septoria_leaf_spot",
        "train/Tomato two spotted spider mites leaf/": "Tomato_Spider_mites_Two_spotted_spider_mite",
        "test/Tomato leaf yellow virus/": "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "test/Tomato leaf mosaic virus/": "Tomato__Tomato_mosaic_virus",
        "test/Tomato leaf/": "Tomato_healthy",
    }
    with zipfile.ZipFile(str(plantdoc_zip_path)) as z:
        for fname in z.namelist():
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            for prefix, target_class in mapping.items():
                if ("PlantDoc-Dataset-master/" + prefix) in fname and target_class in class_to_idx:
                    c_idx = class_to_idx[target_class]
                    try:
                        with z.open(fname) as zfile:
                            img_data = zfile.read()
                            img = Image.open(io.BytesIO(img_data)).convert("RGB").resize((224, 224))
                            images_list.append(np.array(img, dtype=np.float32))
                            labels_list.append(c_idx)
                            paths_list.append(f"zip://{fname}")
                            dataset_names_list.append("PlantDoc_Dataset")
                    except Exception as e:
                        print(f"Failed to read {fname} from zip: {e}")
                    break

X_test = np.array(images_list, dtype=np.float32)
y_true = np.array(labels_list, dtype=int)
total_samples = len(y_true)

print(f"\nCollected total test images: {total_samples}")
classes_present = sorted(list(set(y_true)))
print(f"Unique classes present in test set: {len(classes_present)} out of {num_classes}")

# ============================================================
# DIRECT MODEL INFERENCE & EVALUATION
# ============================================================

print("Running model predictions...")
raw_preds = model.predict(X_test, batch_size=32, verbose=1)

y_pred = np.argmax(raw_preds, axis=1)
confidences = np.max(raw_preds, axis=1)

# Overall Accuracy
overall_acc = float(accuracy_score(y_true, y_pred))
correct_mask = (y_true == y_pred)
correct_count = int(np.sum(correct_mask))
incorrect_count = total_samples - correct_count

# Top-3 and Top-5 accuracy
top3_correct = 0
top5_correct = 0
for i in range(total_samples):
    top3_indices = np.argsort(raw_preds[i])[::-1][:3]
    top5_indices = np.argsort(raw_preds[i])[::-1][:5]
    if y_true[i] in top3_indices:
        top3_correct += 1
    if y_true[i] in top5_indices:
        top5_correct += 1

top3_acc = top3_correct / total_samples
top5_acc = top5_correct / total_samples

# Precision, Recall, F1
precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)

# Per-class metrics
prec_per_class, rec_per_class, f1_per_class, support_per_class = precision_recall_fscore_support(
    y_true, y_pred, labels=list(range(num_classes)), zero_division=0
)

# Per-class accuracy & detailed metrics dictionary
per_class_records = []
for c_idx in range(num_classes):
    c_name = class_names[c_idx]
    c_mask = (y_true == c_idx)
    c_count = int(np.sum(c_mask))
    if c_count > 0:
        c_correct = int(np.sum((y_pred == c_idx) & c_mask))
        c_acc = c_correct / c_count
    else:
        c_correct = 0
        c_acc = 0.0

    per_class_records.append({
        "class_index": c_idx,
        "class_name": c_name,
        "images": c_count,
        "correct": c_correct,
        "accuracy": round(c_acc * 100, 2),
        "precision": round(float(prec_per_class[c_idx]), 4),
        "recall": round(float(rec_per_class[c_idx]), 4),
        "f1": round(float(f1_per_class[c_idx]), 4)
    })

df_per_class = pd.DataFrame(per_class_records)
df_per_class.to_csv(EVAL_DIR / "per_class_metrics.csv", index=False)

# Confidence Analysis
avg_conf_overall = float(np.mean(confidences))
avg_conf_correct = float(np.mean(confidences[correct_mask])) if correct_count > 0 else 0.0
avg_conf_incorrect = float(np.mean(confidences[~correct_mask])) if incorrect_count > 0 else 0.0

# Misclassified Samples
misclassified = []
for i in range(total_samples):
    if not correct_mask[i]:
        misclassified.append({
            "sample_index": i,
            "path": paths_list[i],
            "actual_class": class_names[y_true[i]],
            "predicted_class": class_names[y_pred[i]],
            "confidence": round(float(confidences[i]), 4),
            "dataset": dataset_names_list[i]
        })

df_misclassified = pd.DataFrame(misclassified)
df_misclassified.to_csv(EVAL_DIR / "misclassified_samples.csv", index=False)

# Confusion Matrix Plot
cm = confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))
plt.figure(figsize=(16, 14))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('AgriRakshak Model Confusion Matrix', fontsize=16)
plt.colorbar()
tick_marks = np.arange(num_classes)
plt.xticks(tick_marks, class_names, rotation=90, fontsize=8)
plt.yticks(tick_marks, class_names, fontsize=8)
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('True Label', fontsize=12)
plt.tight_layout()
plt.savefig(EVAL_DIR / "confusion_matrix.png", dpi=300)
plt.close()

# ============================================================
# TEST FASTAPI ENDPOINT (POST /predict)
# ============================================================

print("\nTesting FastAPI /predict endpoint agreement...")
api_url = "http://127.0.0.1:8000/predict"
api_agreements = 0
api_tested = 0
api_results = []

# Test up to 15 sample images across different classes
sample_indices = np.linspace(0, total_samples - 1, num=min(15, total_samples), dtype=int)

for idx in sample_indices:
    fpath = paths_list[idx]
    actual_name = class_names[y_true[idx]]
    direct_pred_name = class_names[y_pred[idx]]
    direct_conf = confidences[idx]
    
    # Extract image bytes
    if fpath.startswith("zip://"):
        zfile_name = fpath.replace("zip://", "")
        with zipfile.ZipFile(str(plantdoc_zip_path)) as z:
            img_bytes = z.read(zfile_name)
    else:
        with open(fpath, "rb") as f:
            img_bytes = f.read()

    try:
        files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
        resp = requests.post(api_url, files=files, timeout=5)
        if resp.status_code == 200:
            res_json = resp.json()
            api_pred_name = res_json.get("predicted_class")
            api_conf = res_json.get("confidence")
            agree = (api_pred_name == direct_pred_name)
            if agree:
                api_agreements += 1
            api_tested += 1
            api_results.append({
                "path": fpath,
                "actual": actual_name,
                "direct_pred": direct_pred_name,
                "api_pred": api_pred_name,
                "direct_conf": round(float(direct_conf), 4),
                "api_conf": api_conf,
                "agrees": agree
            })
    except Exception as e:
        print(f"API test failed for {fpath}: {e}")

api_agreement_rate = (api_agreements / api_tested) if api_tested > 0 else 0.0

# ============================================================
# WEAKEST 5 CLASSES (by F1 score among present classes)
# ============================================================

df_present = df_per_class[df_per_class['images'] > 0].sort_values(by='f1', ascending=True)
weakest_5 = df_present.head(5).to_dict(orient='records')

# Class Imbalance Analysis
df_counts = df_per_class[df_per_class['images'] > 0].sort_values(by='images', ascending=False)
largest_class = df_counts.iloc[0]['class_name']
largest_count = df_counts.iloc[0]['images']
smallest_class = df_counts.iloc[-1]['class_name']
smallest_count = df_counts.iloc[-1]['images']

# ============================================================
# SAVE METRICS JSON
# ============================================================

metrics_dict = {
    "model": "best_agri_finetuned.keras",
    "num_classes": num_classes,
    "datasets_used": ["Rice_and_Maize_Dataset", "PlantDoc_Dataset"],
    "total_test_images": total_samples,
    "correct_predictions": correct_count,
    "incorrect_predictions": incorrect_count,
    "overall_accuracy_pct": round(overall_acc * 100, 2),
    "macro_f1": round(float(f1_macro), 4),
    "weighted_f1": round(float(f1_weighted), 4),
    "macro_precision": round(float(precision_macro), 4),
    "macro_recall": round(float(recall_macro), 4),
    "top3_accuracy_pct": round(top3_acc * 100, 2),
    "top5_accuracy_pct": round(top5_acc * 100, 2),
    "avg_confidence_overall": round(avg_conf_overall, 4),
    "avg_confidence_correct": round(avg_conf_correct, 4),
    "avg_confidence_incorrect": round(avg_conf_incorrect, 4),
    "api_agreement_rate_pct": round(api_agreement_rate * 100, 2),
    "class_imbalance": {
        "largest_class": largest_class,
        "largest_count": int(largest_count),
        "smallest_class": smallest_class,
        "smallest_count": int(smallest_count)
    },
    "weakest_5_classes": weakest_5
}

with open(EVAL_DIR / "metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics_dict, f, indent=4)

# ============================================================
# GENERATE EVALUATION REPORT TEXT
# ============================================================

report_lines = []
report_lines.append("==================================================")
report_lines.append("AGRIRAKSHAK MODEL ACCURACY & PERFORMANCE EVALUATION REPORT")
report_lines.append("==================================================")
report_lines.append(f"MODEL: best_agri_finetuned.keras")
report_lines.append(f"CLASSES: {num_classes}")
report_lines.append(f"DATASETS USED: Rice_and_Maize_Dataset (802 images) + PlantDoc_Dataset (104 images)")
report_lines.append(f"TEST IMAGES: {total_samples}")
report_lines.append(f"CLASSES TESTED: {len(classes_present)} / {num_classes}")
report_lines.append(f"ACCURACY: {round(overall_acc * 100, 2)}%")
report_lines.append(f"MACRO F1: {round(float(f1_macro), 4)}")
report_lines.append(f"WEIGHTED F1: {round(float(f1_weighted), 4)}")
report_lines.append(f"TOP-3 ACCURACY: {round(top3_acc * 100, 2)}%")
report_lines.append(f"TOP-5 ACCURACY: {round(top5_acc * 100, 2)}%")
report_lines.append("")
report_lines.append("--------------------------------------------------")
report_lines.append("1. CONFIDENCE ANALYSIS")
report_lines.append("--------------------------------------------------")
report_lines.append(f"Average Confidence (Overall): {round(avg_conf_overall * 100, 2)}%")
report_lines.append(f"Average Confidence (Correct): {round(avg_conf_correct * 100, 2)}%")
report_lines.append(f"Average Confidence (Incorrect): {round(avg_conf_incorrect * 100, 2)}%")
report_lines.append("")
report_lines.append("--------------------------------------------------")
report_lines.append("2. CLASS IMBALANCE ANALYSIS")
report_lines.append("--------------------------------------------------")
report_lines.append(f"Largest Class: {largest_class} ({largest_count} images)")
report_lines.append(f"Smallest Class (with images): {smallest_class} ({smallest_count} images)")
report_lines.append("Missing Classes (0 images in evaluation set):")
for rec in per_class_records:
    if rec['images'] == 0:
        report_lines.append(f"  - {rec['class_name']}")
report_lines.append("")
report_lines.append("--------------------------------------------------")
report_lines.append("3. FASTAPI ENDPOINT AGREEMENT")
report_lines.append("--------------------------------------------------")
report_lines.append(f"API Tested Samples: {api_tested}")
report_lines.append(f"API-Direct Model Agreement: {round(api_agreement_rate * 100, 2)}%")
report_lines.append("")
report_lines.append("--------------------------------------------------")
report_lines.append("4. WEAKEST 5 CLASSES (BY F1 SCORE)")
report_lines.append("--------------------------------------------------")
for w in weakest_5:
    report_lines.append(f"Class: {w['class_name']}")
    report_lines.append(f"  Images: {w['images']} | Correct: {w['correct']} | Accuracy: {w['accuracy']}%")
    report_lines.append(f"  Precision: {w['precision']} | Recall: {w['recall']} | F1: {w['f1']}")
    report_lines.append("")
report_lines.append("--------------------------------------------------")
report_lines.append("5. PER-CLASS METRICS TABLE")
report_lines.append("--------------------------------------------------")
report_lines.append(f"{'Class':<45} | {'Images':<6} | {'Correct':<7} | {'Accuracy':<8} | {'Precision':<9} | {'Recall':<8} | {'F1':<6}")
report_lines.append("-" * 100)

for rec in per_class_records:
    report_lines.append(
        f"{rec['class_name']:<45} | {rec['images']:<6} | {rec['correct']:<7} | {rec['accuracy']:<7}% | {rec['precision']:<9} | {rec['recall']:<8} | {rec['f1']:<6}"
    )

report_text = "\n".join(report_lines)
with open(EVAL_DIR / "evaluation_report.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print("\nEvaluation report saved to evaluation/evaluation_report.txt")
print(report_text[:1200])
