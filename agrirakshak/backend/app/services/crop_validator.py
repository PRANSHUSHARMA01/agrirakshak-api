import numpy as np
from PIL import Image

def validate_crop_image(image: Image.Image) -> tuple[bool, str]:
    """
    Validates whether an image is a crop/plant leaf photo versus a non-crop image 
    (such as a text document, paper table, screenshot, or random non-agricultural object).
    
    Returns (is_valid, message).
    """
    try:
        img_array = np.array(image.convert("RGB"))
        h, w, _ = img_array.shape
        total_pixels = h * w

        if total_pixels == 0:
            return False, "Invalid image file. Kindly upload a clear photo of a crop or plant leaf."

        # Convert to floating RGB for calculations
        r = img_array[:, :, 0] / 255.0
        g = img_array[:, :, 1] / 255.0
        b = img_array[:, :, 2] / 255.0

        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        delta = max_c - min_c

        # Saturation calculation
        saturation = np.where(max_c == 0, 0, delta / (max_c + 1e-7))
        mean_saturation = float(np.mean(saturation))

        # Check for white / light paper background (typical for documents, invoices, text sheets)
        white_pixels = np.sum((img_array[:, :, 0] > 215) & (img_array[:, :, 1] > 215) & (img_array[:, :, 2] > 215))
        white_ratio = float(white_pixels / total_pixels)

        # Check for dark text / lines
        dark_pixels = np.sum((img_array[:, :, 0] < 60) & (img_array[:, :, 1] < 60) & (img_array[:, :, 2] < 60))
        dark_ratio = float(dark_pixels / total_pixels)

        # Plant leaf greenness / brownness check
        green_dominant = np.sum((img_array[:, :, 1] >= img_array[:, :, 0] - 10) & (img_array[:, :, 1] >= img_array[:, :, 2] - 10))
        brown_dominant = np.sum((img_array[:, :, 0] > img_array[:, :, 2]) & (img_array[:, :, 1] > img_array[:, :, 2] * 0.7) & (img_array[:, :, 0] < 220))
        plant_color_ratio = float((green_dominant + brown_dominant) / total_pixels)

        # Rule 1: High white ratio -> document / paper page
        if white_ratio > 0.55:
            return False, "Image appears to be a document or paper text. Kindly upload a clear photo of a crop or plant leaf."

        # Rule 2: Low saturation with high background & dark text -> document / table / screenshot
        if white_ratio > 0.35 and mean_saturation < 0.18 and dark_ratio < 0.35:
            return False, "Non-crop photo detected (low color saturation). Kindly upload a clear photo of a crop or plant leaf."

        # Rule 3: Extremely low overall saturation -> monochrome / document / non-biological
        if mean_saturation < 0.08:
            return False, "Monochrome or non-plant image detected. Kindly upload a clear photo of a crop or plant leaf."

        # Rule 4: Very low organic plant/crop color distribution
        if plant_color_ratio < 0.12 and white_ratio > 0.25:
            return False, "No leaf or crop features detected in photo. Kindly upload a clear photo of a crop or plant leaf."

        return True, "Valid crop photo"
    except Exception as e:
        print(f"[CropValidator] Validation error: {e}")
        return True, "Valid crop photo"
