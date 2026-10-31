# AgriFact-Checker: Farm-Scheme & Advisory Misinformation Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Tests: Passing](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg)](tests/)

A web-based verification and fact-checking tool designed to protect farmers, Farmer Producer Organizations (FPOs), and rural communities from fraudulent agricultural schemes, deceptive subsidy forwards, fake crop advisories, and malicious phishing links.

---

## 📌 Table of Contents
- [Key Features](#-key-features)
- [Architecture & Technical Design](#-architecture--technical-design)
- [Tech Stack](#-tech-stack)
- [Environment Configuration](#-environment-configuration)
- [Installation & Quick Start](#-installation--quick-start)
- [Running the Application](#-running-the-application)
- [Training & Evaluating the ML Model (Optional)](#-training--evaluating-the-ml-model-optional)
- [Running Automated Tests](#-running-automated-tests)
- [Datasets & Sample Test Cases](#-datasets--sample-test-cases)
- [Model Scope & Limitations](#-model-scope--limitations)
- [License](#-license)

---

## 🚀 Key Features

1. **Multi-Modal Claim Ingestion:** Verify raw text forwards or upload WhatsApp poster/flyer screenshots directly.
2. **Flyer OCR Engine:** Automated text extraction from uploaded images using Pillow and Tesseract OCR.
3. **Calibrated Machine Learning:** Hybrid word & character n-gram TF-IDF vectorizer paired with a calibrated Logistic Regression classifier to avoid overconfident predictions.
4. **Pre-Trained & Zero-Setup:** Serialized model binaries (`classifier.joblib` & `vectorizer.joblib`) are pre-trained and committed with self-healing auto-train fallbacks on launch.
5. **Evaluator Sample Pre-fills:** Instant 1-click test buttons (`Genuine Scheme`, `Phishing Scam`, `Commercial Link`) built directly into the UI for rapid testing.
6. **Domain Trust-Fusion:** Validates URLs against official Indian government portals (`.gov.in`, `.nic.in`), boosting confidence for genuine portals and penalizing unverified domains.
7. **Scam Mobile Heuristic Alerts:** Detects private 10-digit mobile numbers used in advance-fee scams and surfaces dedicated warnings.
8. **Scheme Auto-Matching:** Cross-references claims against known central and state agricultural schemes (e.g., PM-KISAN, PMFBY, PM-KUSUM) via SQLite FTS5 search.
9. **Transparent Explainability:** Displays the most influential terms driving each verdict.
10. **Audit Trail & Feedback:** Persists check history and captures user upvote/downvote feedback in SQLite.

---

## 🏛 Architecture & Technical Design

For the complete architectural diagrams, ML dataflow, SQLite schemas, and endpoint specifications, please refer to:
👉 [**Technical Design Document (`docs/TECHNICAL_DESIGN.md`)**](docs/TECHNICAL_DESIGN.md)

---

## 🛠 Tech Stack

- **Backend:** Flask, Python 3.11+
- **Machine Learning:** Scikit-learn (TF-IDF FeatureUnion + CalibratedClassifierCV with Logistic Regression), Joblib, NumPy, Pandas
- **OCR Engine:** Pillow, Pytesseract / Tesseract-OCR
- **Database:** SQLite3 with FTS5 Full-Text Search
- **Frontend:** Responsive HTML5, CSS3, JavaScript
- **Testing:** Pytest

---

## ⚙ Environment Configuration

AgriFact-Checker works out of the box with sensible defaults, but supports environment variable customization via `.env`.

1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```
2. Available configuration options in `.env`:
   - `FLASK_APP`: Application entrypoint (default: `app.py`)
   - `FLASK_SECRET_KEY`: Session and CSRF secret key
   - `DATABASE_PATH`: Custom path to SQLite database (default: `instance/checker.db`)
   - `MODEL_PATH`: Path to serialized classifier artifact (default: `model/classifier.joblib`)
   - `VECTORIZER_PATH`: Path to serialized TF-IDF vectorizer (default: `model/vectorizer.joblib`)
   - `VERIFIED_DOMAINS_PATH`: Path to verified government domains whitelist JSON (default: `config/verified_domains.json`)
   - `MAX_INPUT_LENGTH`: Maximum allowable input character limit (default: `5000`)

---

## 📦 Installation & Quick Start

### 1. Prerequisites
- Python 3.11 or newer
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/sngaryan/AgriFact-Checker.git
cd AgriFact-Checker
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** Pre-trained model artifacts are **already included** in `model/`. You do not need to run a training script before launching the app!

### 4. (Optional) Install Tesseract OCR Engine for Flyer Extraction
To enable automated text extraction from uploaded images/posters:
- **Windows:** Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Ensure `C:\Program Files\Tesseract-OCR` is in your System PATH.
- **Ubuntu/Debian:**
  ```bash
  sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-hin
  ```
- **macOS:**
  ```bash
  brew install tesseract tesseract-lang
  ```

---

## 💻 Running the Application

Launch the Flask development server:
```bash
python app.py
```
Or via the Flask CLI:
```bash
flask --app app run
```
Open your browser and navigate to **`http://127.0.0.1:5000`**.

System health status can be queried at **`http://127.0.0.1:5000/health`**.

---

## 🧠 Training & Evaluating the ML Model (Optional)

The pre-trained model is already included in `model/`. If you wish to retrain or experiment with new dataset splits, run:
```bash
python scripts/train_model.py
```
This script processes datasets from `data/processed/`, trains both Calibrated Logistic Regression and a Naive Bayes baseline, outputs a comparison table, and saves the binary artifacts to:
- `model/classifier.joblib`
- `model/vectorizer.joblib`
- `model/metrics.json`

---

## 🧪 Running Automated Tests

Run the full pytest test suite across database, ML predictor, OCR fallback, topic checks, and API endpoints:
```bash
python -m pytest
```
All 26 test cases are located in the [`tests/`](tests/) directory:
- [`tests/test_app.py`](tests/test_app.py): Flask routes, input validation, and rendering
- [`tests/test_predictor.py`](tests/test_predictor.py): ML model inference, domain trust-fusion, and explainability
- [`tests/test_domain_check.py`](tests/test_domain_check.py): URL parsing, whitelist checks, and phone heuristic detection
- [`tests/test_database.py`](tests/test_database.py): SQLite creation, insertion, and retrieval
- [`tests/test_topic_checker.py`](tests/test_topic_checker.py): Agricultural domain relevance checks
- [`tests/test_ocr.py`](tests/test_ocr.py): Flyer image text extraction & error resilience

---

## 📊 Datasets & Sample Test Cases

Explore the data assets and test examples:
- [**Dataset Documentation & Card (`data/DATASET_CARD.md`)**](data/DATASET_CARD.md): Details data sources, annotations, and split ratios.
- [**Raw Agricultural Messages (`data/custom_agri_messages.csv`)**](data/custom_agri_messages.csv): Curated agricultural messages with scheme labels and truth status.
- [**Processed Training Splits (`data/processed/`)**](data/processed/): Split datasets (`train.csv`, `val.csv`, `test.csv`, `full_dataset.csv`).

### Quick Test Cases to Try in the UI:
You can click the 💡 **Try an example** buttons directly in the web UI, or test these manually:
- **Genuine Scheme Example:**
  > *"Under the PM-KISAN scheme, eligible landholding farmer families receive a financial benefit of Rs 6000 per year paid in three installments. Verify details at official portal pmkisan.gov.in."*
- **Phishing / Fraud Example:**
  > *"Urgent! 80% subsidy announced on solar water pumps and tractors. Register immediately by paying Rs 500 at pm-solar-subsidy.in or contact helpline 9876543210."*
- **Out of Domain Example:**
  > *"Click here to get a discount voucher for international air tickets."*

---

## ⚠️ Model Scope & Limitations

1. **Language Scope:** Currently optimized for English and Romanized Hindi (Hinglish). While character n-grams handle common Hinglish variations, regional Devanagari script processing depends on OCR language packs and will be expanded in future versions.
2. **Domain Focus:** The model is intentionally tuned for Indian agriculture and rural schemes. Non-agricultural claims are categorized as `out_of_domain` rather than fact-checked.
3. **Domain Whitelist Dependency:** The trust-fusion system matches official portals against `config/verified_domains.json`. Newly launched state portals must be registered in this whitelist to receive the verified trust boost.
4. **Advisory Verification:** For real-time agronomic advice (e.g., localized pesticide dosages during an active pest outbreak), farmers should always cross-verify recommendations with local Krishi Vigyan Kendra (KVK) scientists or state extension officers.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
