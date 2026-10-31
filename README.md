# 🌿 AgriFact-Checker: Farm-Scheme & Advisory Misinformation Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Tests: Passing](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg)](tests/)

An AI-powered verification tool designed to protect farmers, Farmer Producer Organizations (FPOs), and rural communities from fraudulent agricultural schemes, deceptive WhatsApp forwards, fake subsidy notices, and advance-fee phishing scams.

---

## 📌 Table of Contents
- [Key Features](#-key-features)
- [Quick Start & Setup](#-quick-start--setup)
- [How to Test the Application](#-how-to-test-the-application)
- [Automated Tests](#-automated-tests)
- [Architecture & Technical Design](#-architecture--technical-design)
- [Datasets & Sample Data](#-datasets--sample-data)
- [Scope & Limitations](#-scope--limitations)
- [License](#-license)

---

## 🚀 Key Features

- **Multi-Modal Verification:** Ingests raw claim text or scanned WhatsApp flyer/poster screenshots.
- **Bilingual Flyer OCR:** Extracts text in both **Hindi (Devanagari)** and **English** using Tesseract and Pillow with bundled language models.
- **Calibrated ML Classification:** Hybrid word & character n-gram TF-IDF vectorizer paired with a calibrated Logistic Regression classifier to avoid overconfident predictions.
- **Domain Trust-Fusion:** Cross-verifies links against official Indian government portals (`.gov.in`, `.nic.in`), granting confidence boosts to authentic sources and penalizing unverified sites.
- **Scam Mobile & UPI Heuristics:** Detects private mobile numbers (including `+91`, spaces, hyphens) and unauthorized payment handles (`UPI no.`, `GPay`, `Paytm`, `PhonePe`) frequently used in advance-deposit fraud.
- **Scheme Matching & Explainability:** Identifies official matching schemes (PM-KISAN, KCC, Natural Farming Mission, etc.) via SQLite FTS5 search and highlights the influential keywords driving each verdict.
- **Audit History & Feedback:** Persists check history and collects farmer feedback in an embedded SQLite database.

---

## 📦 Quick Start & Setup

Follow these simple steps to run the application locally on your machine:

### 1. Prerequisites
- **Python 3.11 or newer** installed
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/sngaryan/AgriFact-Checker.git
cd AgriFact-Checker
```

### 3. Create & Activate Virtual Environment
Isolates dependencies cleanly:

- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **On Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** Pre-trained model binaries (`classifier.joblib`, `vectorizer.joblib`) are **already included** in `model/`. You can launch the application immediately without training!

### 5. Launch the Application
```bash
python app.py
```
Open your web browser and go to:  
👉 **`http://127.0.0.1:5000`**

*(Health check endpoint is available at `http://127.0.0.1:5000/health`)*

---

### 6. (Optional) Install Tesseract OCR Engine for Flyer Extraction
Text claim verification works 100% standalone. If you wish to test scanning WhatsApp flyer images locally:
- **Windows:** Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Ensure `C:\Program Files\Tesseract-OCR` is installed or in your System PATH.
- **Ubuntu/Debian:** `sudo apt update && sudo apt install -y tesseract-ocr`
- **macOS:** `brew install tesseract`

*(Bilingual language models for **English and Hindi** are already bundled inside [`model/tessdata/`](model/tessdata) and are loaded automatically by the application.)*

---

## 🧪 How to Test the Application

Once the dashboard is open in your browser, you can evaluate the prototype using either of two methods:

### Method A: Instant 1-Click Sample Buttons (Fastest)
Directly under the text input area on the homepage, click any of the sample pills:
- **`🛡️ Genuine Scheme`** $\rightarrow$ Pre-fills an authentic PM-KISAN message linking to `pmkisan.gov.in`. (Verdict: **Likely Genuine**).
- **`⚠️ Phishing Scam`** $\rightarrow$ Pre-fills a fake tractor subsidy scam with an advance fee and helpline number. (Verdict: **Likely Misleading** with scam alert).
- **`🏷️ Commercial Link`** $\rightarrow$ Pre-fills an unverified private retail store link. (Verdict: **Commercial Promo**).

### Method B: Uploading Real Sample Flyers
Drag and drop any of the real-world sample posters from [`data/sample_flyers/`](data/sample_flyers):
- **`fake_flyer_1_upi_scam.jpg`**: Fake government scheme poster asking for a ₹2,500 deposit via UPI $\rightarrow$ Flags as **Likely Misleading** with a **Private Mobile / UPI Scam Alert**.
- **`fake_flyer_2_canada_visa_scam.jpg`**: Deceptive overseas farm job advertisement with advance processing fees $\rightarrow$ Flags as **Misleading**.
- **`official_flyer_1_kcc_subsidy.jpg`**: Official Ministry Kisan Credit Card (KCC) announcement $\rightarrow$ Flags as **Likely Genuine**.
- **`official_flyer_2_natural_farming.jpg`**: Official Hindi Natural Farming Mission infographic $\rightarrow$ Verified via **Hindi Devanagari OCR** as **Likely Genuine**.

---

## 🔬 Automated Tests

Verify that all database operations, ML inferences, domain security checks, and OCR routines pass:
```bash
python -m pytest
```
All **26 unit and integration tests** are passing across the test suite:
- [`tests/test_app.py`](tests/test_app.py): Flask routing, payload validation, and UI template rendering.
- [`tests/test_predictor.py`](tests/test_predictor.py): ML inference, trust-fusion confidence boosting, and explainability.
- [`tests/test_domain_check.py`](tests/test_domain_check.py): Whitelist domain matching, phishing regex, and phone/UPI detection.
- [`tests/test_database.py`](tests/test_database.py): SQLite creation, insertion, retrieval, and feedback recording.
- [`tests/test_topic_checker.py`](tests/test_topic_checker.py): Agricultural domain relevance guardrails.
- [`tests/test_ocr.py`](tests/test_ocr.py): Image text extraction and fallback handling.

---

## 🏛 Architecture & Technical Design

For the complete end-to-end system design, please read:  
👉 [**Technical Design Document (`docs/TECHNICAL_DESIGN.md`)**](docs/TECHNICAL_DESIGN.md)

- **System Architecture Flow:** User $\rightarrow$ OCR Preprocessing $\rightarrow$ Security Heuristics $\rightarrow$ Calibrated ML $\rightarrow$ Trust Fusion $\rightarrow$ SQLite.
- **Database Schema:** Documented schema tables for `checks`, `feedback`, and `schemes_search` (SQLite FTS5).
- **Environment Overrides (Optional):** Copy `.env.example` to `.env` to customize database paths, port numbers, or secret keys.
- **Model Retraining (Optional):** Run `python scripts/train_model.py` to retrain and calibrate the scikit-learn models on custom data splits.

---

## 📊 Datasets & Sample Data

- [**Dataset Documentation & Card (`data/DATASET_CARD.md`)**](data/DATASET_CARD.md): Details data provenance, annotation methods, and split distributions.
- [**Curated Agricultural Messages (`data/custom_agri_messages.csv`)**](data/custom_agri_messages.csv): Annotated dataset of real agricultural claims.
- [**Sample Flyer Posters (`data/sample_flyers/`)**](data/sample_flyers): Real-world fake and official posters for multimodal OCR evaluation.
- [**Processed Training Splits (`data/processed/`)**](data/processed/): Stratified train, validation, and test splits.

---

## ⚠️ Scope & Limitations

1. **Language Scope:** The text classification model is trained on English and Romanized Hindi (Hinglish) agricultural messages. Image OCR supports both English and Hindi (Devanagari script).
2. **Domain Focus:** The system is specifically optimized for Indian agriculture and government rural schemes. Non-agricultural claims are categorized as `out_of_domain`.
3. **Advisory Verification:** For localized agrochemical dosages or pest outbreak treatments, farmers should always confirm recommendations with local Krishi Vigyan Kendra (KVK) scientists or state extension officers.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
