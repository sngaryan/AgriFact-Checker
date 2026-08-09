import os
import io
import shutil
import re
from PIL import Image, ImageEnhance, ImageFilter

# Common standard installation paths for Tesseract binary across OS platforms
POSSIBLE_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
    os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/opt/homebrew/bin/tesseract"
]

def _configure_tesseract():
    """Detect and configure tesseract command path if not in system PATH."""
    try:
        import pytesseract
        # If tesseract is already found in PATH, return True
        if shutil.which("tesseract"):
            return True
            
        # Check common standard installation paths
        for path in POSSIBLE_TESSERACT_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
    except Exception:
        pass
    return False

def preprocess_image(img: Image.Image) -> Image.Image:
    """Preprocess flyer images to maximize OCR accuracy on WhatsApp screenshots/graphics."""
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    
    # Upscale low-res flyer graphics (target width min 1800px)
    if width < 1800:
        scale_factor = 1800.0 / float(width)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    # Contrast enhancement
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    
    # Sharpness enhancement
    sharpener = ImageEnhance.Sharpness(img)
    img = sharpener.enhance(1.5)
    
    return img

def clean_ocr_text(text: str) -> str:
    """Clean up common OCR noise artifacts while preserving words and URLs."""
    if not text:
        return ""
    # Normalize multiple line breaks and spaces
    cleaned = re.sub(r'[ \t]+', ' ', text)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def extract_text_from_image(file_storage) -> dict:
    """Extract text from an uploaded flyer/poster image using PIL and Pytesseract OCR."""
    if not file_storage or not file_storage.filename:
        return {"text": "", "success": False, "message": "No file uploaded."}
        
    try:
        image_bytes = file_storage.read()
        if not image_bytes:
            return {"text": "", "success": False, "message": "Empty file."}
            
        original_img = Image.open(io.BytesIO(image_bytes))
        preprocessed_img = preprocess_image(original_img)
        
        # Check if Tesseract engine is installed and configured
        tesseract_available = _configure_tesseract()
        
        if tesseract_available:
            import pytesseract
            extracted_results = []
            
            # Pass 1: Try preprocessed image with Hindi + English or default
            for target_img in [preprocessed_img, original_img]:
                for config_args in ['--psm 3', '--psm 11', '--psm 6']:
                    try:
                        try:
                            res = pytesseract.image_to_string(target_img, lang='hin+eng', config=config_args)
                        except Exception:
                            res = pytesseract.image_to_string(target_img, config=config_args)
                            
                        cleaned = clean_ocr_text(res)
                        if cleaned and len(cleaned) > 5:
                            extracted_results.append(cleaned)
                    except Exception:
                        pass
                        
            if extracted_results:
                # Choose the longest / richest extracted text result
                best_text = max(extracted_results, key=len)
                return {
                    "text": best_text,
                    "success": True,
                    "message": "Text successfully extracted from image via Tesseract OCR."
                }
            else:
                return {
                    "text": "",
                    "success": False,
                    "message": "Image received, but no readable text could be extracted from this photo. Please try a clearer flyer image or paste the text directly."
                }

        # Secondary fallback: Attempt EasyOCR if installed
        try:
            import easyocr
            reader = easyocr.Reader(['en', 'hi'], gpu=False)
            results = reader.readtext(image_bytes, detail=0)
            extracted_text = clean_ocr_text(" ".join(results))
            if extracted_text:
                return {
                    "text": extracted_text,
                    "success": True,
                    "message": "Text successfully extracted from image via EasyOCR."
                }
        except Exception:
            pass
            
        # If Tesseract binary is not installed at all on server host
        return {
            "text": "",
            "success": False,
            "message": (
                "Image received, but Tesseract OCR engine is not installed on this server. "
                "To enable flyer OCR, install Tesseract-OCR (Windows installer: https://github.com/UB-Mannheim/tesseract/wiki, "
                "Linux: sudo apt install tesseract-ocr) or type/paste the message text directly."
            )
        }
        
    except Exception as e:
        return {"text": "", "success": False, "message": f"Could not process image: {str(e)}"}
