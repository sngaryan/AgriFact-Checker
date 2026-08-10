# Backend Implementation Overview & Work Summary

This document provides a detailed summary of all backend work completed across the workspace, focusing on architecture, database storage, API endpoints, Machine Learning integration, explainability services, and verification test suites.

---

## 1. AgriFact-Checker Backend Architecture (`c:/Users/shiva/agritech/AgriFact-Checker`)

The backend for **AgriFact-Checker** is a Python Flask web application integrated with scikit-learn ML models and an SQLite storage engine.

```
AgriFact-Checker Backend
├── app.py                      # Flask Application Routes & Endpoints
├── config.py                   # Centralized Configuration & Environment Paths
├── services/
│   ├── database.py             # SQLite Persistence Engine & Query Layer
│   ├── predictor.py            # ML Model Loading, Inference & Explainability
│   └── domain_check.py          # Trust-List Domain Verification & URL Extraction
├── scripts/
│   ├── prepare_data.py         # Data Preprocessing & Pipeline Scripts
│   └── train_model.py          # TF-IDF + Logistic Regression Model Training Script
└── tests/                      # Pytest Automated Test Suite
    ├── test_app.py
    ├── test_database.py
    ├── test_domain_check.py
    └── test_predictor.py
```

---

### Core Components & Work Completed

#### A. Web Application Server & API Routes (`app.py`)
- **Main Interface Route (`GET /`)**: Loads and renders the index UI, retrieving the 10 most recent check records from the SQLite database.
- **Verification Engine Endpoint (`POST /check`)**:
  - Validates submitted message text (handles empty input, trims whitespace, enforces `MAX_INPUT_LENGTH = 5000` limit).
  - Triggers domain trust analysis via `services/domain_check.py`.
  - Executes fake news classification and keyword extraction via `services/predictor.py`.
  - Saves completed checks into SQLite and returns rendered results card with prediction metrics.
  - Implements graceful exception handling for un-trained model scenarios.
- **Feedback Capture Endpoint (`POST /feedback/<check_id>`)**:
  - Accepts user feedback (`upvote` or `downvote`) for stored claim checks.
  - Persists vote entries linked to the specific check ID with ISO UTC timestamps.
- **Health Check Endpoint (`GET /health`)**:
  - Evaluates system status: Database connectivity check and ML model load state check.
  - Returns structured JSON response (`status`, `database`, `model`).

#### B. Machine Learning & Explainability Engine (`services/predictor.py`)
- **Model Loader (`load_model()`)**: Lazy-loads serialized TF-IDF vectorizer (`vectorizer.joblib`) and Logistic Regression classifier (`classifier.joblib`).
- **Inference & Scoring (`predict()`)**:
  - Vectorizes raw text inputs into TF-IDF feature space.
  - Calculates predicted category label (`genuine` vs `misleading`).
  - Computes probability confidence percentage score.
- **Explainability Keyword Extraction**:
  - Tokenizes input text into distinct words.
  - Extracts Logistic Regression feature coefficients (`_classifier.coef_`).
  - Calculates contribution score for each word: $\text{Contribution} = \text{TF-IDF Weight} \times \text{Class Coefficient}$.
  - Filters and ranks the top 3–5 most influential keywords driving the prediction.
  - Includes a TF-IDF fallback vector ranker for cases where feature alignment is neutral.

#### C. Persistence Layer & Database Engine (`services/database.py`)
- **Database Engine**: Uses SQLite (`instance/checker.db`) with `sqlite3.Row` dictionary mapping.
- **Schema Initializer (`init_db()`)**:
  - `checks` table: `id`, `submitted_text`, `predicted_label`, `confidence`, `influential_terms` (JSON text), `detected_domain`, `domain_status`, `created_at`.
  - `feedback` table: `id`, `check_id` (foreign key to `checks`), `vote`, `created_at`.
- **Database Operations**:
  - `save_check()`: Persists structured prediction payloads and returns autoincremented check IDs.
  - `get_recent_checks(limit)`: Fetches recent history items sorted by newest ID first, parsing JSON terms.
  - `save_feedback(check_id, vote)`: Validates check existence and records feedback entries.

#### D. Domain Extraction & Trust Verification Service (`services/domain_check.py`)
- **URL Extraction**: Uses compiled regex patterns (`http://`, `https://`, `www.`) to extract host links from unstructured message text.
- **Domain Normalization**: Utilizes `urllib.parse.urlparse` to isolate clean hostname paths, stripping port numbers and sub-path prefixes.
- **Whitelist Matching**:
  - Loads government whitelist from `config/verified_domains.json` (e.g. `pmkisan.gov.in`, `agriwelfare.gov.in`, `gov.in`).
  - Validates exact host match or exact subdomain suffix match.
  - Categorizes status as `verified`, `not_in_list`, or `no_domain_found`.

#### E. Data Pipelines & Model Training Scripts (`scripts/`)
- **`prepare_data.py`**: Reads raw datasets, cleans noise/duplicates, blends agricultural scheme data, and creates stratified train/test split datasets.
- **`train_model.py`**: Trains TF-IDF + Logistic Regression pipeline, computes evaluation metrics (Accuracy, Precision, Recall, F1, Confusion Matrix), and exports model joblib artifacts to `model/`.

#### F. Automated Backend Testing Suite (`tests/`)
- **`test_app.py`**: Integrates Flask test client to verify HTTP status codes, form validations, health endpoint response, and feedback handling.
- **`test_database.py`**: Validates table creation, insert queries, recent check ordering, and foreign key integrity.
- **`test_predictor.py`**: Validates model lazy loading, classification labels, confidence range [0-100%], and influential term generation.
- **`test_domain_check.py`**: Verifies URL parsing regex, whitelist sub-domain matching, and edge case lookalike domain filtering.

---

## 2. Campus Digital Twin Backend Summary (`c:/Users/shiva/cc/backend`)

In addition to AgriFact-Checker, backend architecture for the **Digital Twin Campus Roadmap** project was structured under `cc/backend`:

- **Framework**: FastAPI application with `uvicorn` runner (`run.py`, `app/main.py`).
- **Database**: SQLite database engine (`campus_digital_twin.db`) configured with SQLAlchemy (`app/database.py`) and pre-populated seed scripts (`app/seed.py`).
- **Modular Route Controllers (`app/routes/`)**:
  - `auth.py`: User authentication endpoints.
  - `buildings.py`: Campus building location & metadata APIs.
  - `rooms.py`: Room allocation, occupancy, and status endpoints.
  - `events.py`: Campus event scheduling routes.
  - `maintenance.py`: Issue reporting & maintenance task tracking APIs.
  - `navigation.py`: Pathfinding & route calculation services.
  - `analytics.py`: Campus utilization & occupancy analytics.
  - `ml_prediction.py`: Machine learning occupancy prediction service.
  - `websockets.py`: Real-time WebSocket event streaming.

---

## Summary Status

| Module | Status | Core Functionality |
| :--- | :---: | :--- |
| **Flask App Routes** | ✅ Complete | Form handling, result rendering, feedback & health endpoints |
| **ML Predictor** | ✅ Complete | TF-IDF + Logistic Regression inference & keyword explainability |
| **SQLite Storage** | ✅ Complete | Schema design, CRUD operations, check history & feedback log |
| **Domain Checker** | ✅ Complete | Regex URL parsing & verified government domain whitelist matching |
| **Training Pipeline** | ✅ Complete | Data preprocessing, TF-IDF model training & metrics export |
| **Pytest Suite** | ✅ Complete | Full unit & integration test coverage across app, DB, ML & domain modules |
