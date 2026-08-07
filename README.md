# Farm-Scheme & Advisory Misinformation Checker

A web-based tool designed to help farmers assess forwarded messages, claims, and links regarding government agricultural schemes, subsidies, and cultivation advice.

## Tech Stack
- **Backend:** Flask, Python
- **Machine Learning:** Scikit-learn (TF-IDF + Logistic Regression)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## Installation and Setup

### 1. Prerequisites
- Python 3.11 or newer

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Training the Model
```bash
python scripts/train_model.py
```

### 4. Running the Web Application
```bash
flask --app app run
```

### 5. Running Tests
```bash
pytest
```
