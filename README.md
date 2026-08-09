# Farm-Scheme & Advisory Misinformation Checker

A web-based tool designed to help farmers assess forwarded messages, claims, and links regarding government agricultural schemes, subsidies, and cultivation advice.

## Tech Stack
- **Backend:** Flask, Python
- **Machine Learning:** Scikit-learn (TF-IDF + Logistic Regression)
- **OCR Engine:** Pillow, Pytesseract / Tesseract-OCR
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## Installation and Setup

### 1. Prerequisites
- Python 3.11 or newer

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install Tesseract OCR Engine for Flyer Extraction
To enable automatic text extraction from uploaded WhatsApp flyer images/posters:
- **Windows:** Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Add `C:\Program Files\Tesseract-OCR` to your System PATH or install to default path.
- **Ubuntu/Debian:** 
  ```bash
  sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-hin
  ```
- **macOS:** 
  ```bash
  brew install tesseract tesseract-lang
  ```

### 4. Training the Model
```bash
python scripts/train_model.py
```

### 5. Running the Web Application
```bash
flask --app app run
```

### 6. Running Tests
```bash
pytest
```
