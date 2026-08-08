# Dataset Card & Model Evaluation Report

## 1. Overview & Problem Context

This dataset and classification pipeline serve the **Farm-Scheme & Agriculture Advisory Misinformation Checker** application. The system assists farmers, extension workers, and rural citizens in assessing agricultural WhatsApp messages, viral social media claims, and government scheme announcements.

The classifier categorizes text into two primary categories:
- **`genuine`**: Legitimate government scheme announcements, official extension advisories, verified portal links (e.g., PM-KISAN, PMFBY, KCC, e-NAM, Soil Health Card), and scientific farming practices.
- **`misleading`**: Phishing scams, fake subsidy offers, fake tractor/pump giveaways, misinformation on fertilizer bans, unverified home remedies/fake pest advisories, and financial fraud attempts.

> [!IMPORTANT]
> **Advisory Disclaimer**: The output of this ML model represents a probabilistic risk signal based on text features, **not an absolute or official factual determination**. Users should verify high-risk claims against official portals (`.gov.in`, `.nic.in`) or contact local agriculture officers.

---

## 2. Dataset Provenance & Sources

The training corpus consists of two curated data sources:

1. **Curated Agriculture & Scheme Dataset (`data/custom_agri_messages.csv`)**:
   - **Provenance**: Created specifically for this project by synthesizing real-world WhatsApp forwards, phishing SMS messages targeting farmers, official Indian Ministry of Agriculture press releases, ICAR advisories, and government scheme guidelines (PM-Kisan, PMFBY, KCC, e-NAM, SMAM, PKVY).
   - **Content**: 40 curated records (20 genuine, 20 misleading).
   - **License**: Open Data / CC-BY 4.0 for educational and research use.

2. **Supplementary News & Announcement Dataset (`data/raw/public_fake_news_supplement.csv`)**:
   - **Provenance**: Public domain news headlines and viral misinformation statements covering telecom scams, banking alerts, public utility notices, and government announcements.
   - **Content**: 40 supplementary records (20 genuine, 20 misleading).
   - **License**: Public Domain / CC0.

---

## 3. Data Cleaning & Splitting Methodology

The data pipeline in [`scripts/prepare_data.py`](file:///c:/Users/shiva/agritech/AgriFact-Checker/scripts/prepare_data.py) executes the following preprocessing steps:
1. **Trimming & Normalization**: Leading/trailing whitespace is removed. Labels are lowercased and mapped strictly to `genuine` and `misleading`.
2. **Deduplication**: Duplicate text strings are filtered to prevent data leakage between splits.
3. **Stratified Split**: The cleaned dataset is partitioned using a 70% / 15% / 15% stratified split (`random_state=42`):
   - **Train set** (`data/processed/train.csv`): 56 samples (50% genuine, 50% misleading)
   - **Validation set** (`data/processed/val.csv`): 12 samples (50% genuine, 50% misleading)
   - **Test set** (`data/processed/test.csv`): 12 samples (50% genuine, 50% misleading)

---

## 4. Model Training & Baseline Evaluation

Model training and evaluation are conducted via [`scripts/train_model.py`](file:///c:/Users/shiva/agritech/AgriFact-Checker/scripts/train_model.py).

### Models Evaluated:
1. **Primary Model**: TF-IDF Vectorizer (max 5,000 features, 1-2 n-grams) + Logistic Regression ($C=1.0, \text{random\_state}=42$).
2. **Baseline Model**: TF-IDF Vectorizer + Multinomial Naive Bayes ($\alpha=1.0$).

### Evaluation Metrics (Held-Out Test Set):

| Metric | Logistic Regression | Multinomial Naive Bayes (Baseline) |
|---|---|---|
| **Accuracy** | **1.0000** | 1.0000 |
| **Precision (`misleading`)** | **1.0000** | 1.0000 |
| **Recall (`misleading`)** | **1.0000** | 1.0000 |
| **F1-Score (`misleading`)** | **1.0000** | 1.0000 |
| **F1-Score (Macro)** | **1.0000** | 1.0000 |

### Confusion Matrix (Logistic Regression on Test Set):
```text
                  Predicted Genuine   Predicted Misleading
Actual Genuine            6                    0
Actual Misleading         0                    6
```

### Model Selection Rationale:
Logistic Regression was selected as the deployed classifier because its linear coefficients ($\boldsymbol{\beta}$) directly map to feature log-odds, enabling transparent keyword contribution scoring (`influential_terms`) in [`services/predictor.py`](file:///c:/Users/shiva/agritech/AgriFact-Checker/services/predictor.py).

---

## 5. Artifacts Exported

The training script automatically exports the following files:
- **Classifier**: [`model/classifier.joblib`](file:///c:/Users/shiva/agritech/AgriFact-Checker/model/classifier.joblib)
- **Vectorizer**: [`model/vectorizer.joblib`](file:///c:/Users/shiva/agritech/AgriFact-Checker/model/vectorizer.joblib)
- **Metrics Report**: [`model/metrics.json`](file:///c:/Users/shiva/agritech/AgriFact-Checker/model/metrics.json)

---

## 6. Known Limitations & Caveats

1. **Vocabulary Coverage**: The model relies on n-gram TF-IDF representations. Out-of-vocabulary (OOV) terms in newly emergent scams may receive neutral weights.
2. **Language Scope**: Current dataset contains English and Hinglish Romanized scheme text. Regional language scripts (Hindi, Marathi, Punjabi, Telugu, Tamil, etc.) require separate tokenization or multilingual embeddings in future iterations.
3. **Adversarial Evasion**: Typos or intentionally misspelled words (e.g., `P.M-K1san`, `subsidyyy`) might bypass keyword matching.
4. **Temporal Drift**: Subsidy rules and government schemes change over time. The training set should be updated periodically to maintain recency.
