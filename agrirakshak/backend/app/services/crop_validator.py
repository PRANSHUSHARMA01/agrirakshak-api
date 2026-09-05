from PIL import Image

def validate_crop_image(image: Image.Image) -> tuple[bool, str]:
    """
    Validation disabled as requested by user. Always accepts all uploaded images.
    """
    return True, "Valid crop photo"
