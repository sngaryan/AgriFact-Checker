# Farm-Scheme & Advisory Misinformation Checker

## Implementation Plan

### Problem understanding

The tool helps farmers assess forwarded messages about government agriculture schemes, subsidies and cultivation advice. Users paste a WhatsApp message or headline. A text-classification model returns **Likely Genuine** or **Likely Misleading**, a model-confidence percentage, and the words that most influenced that result. The app also records previous checks and optional user feedback.

The result is a risk signal, not an official fact-check. A message from an official-looking domain can still be wrong or outdated, and an unlisted domain is not automatically false.

### MVP features

1. Paste text into a web form.
2. Classify it using TF-IDF features with Logistic Regression.
3. Display label and confidence score.
4. Highlight the three to five influential keywords.
5. Check any URL against a small hardcoded list of verified government portals.
6. Store checks in a history table.
7. Add upvote/downvote feedback that is logged but does not retrain the model.

### Recommended stack

- Backend: Python + Flask
- ML: scikit-learn, TF-IDF Vectorizer, Logistic Regression
- Baseline: Multinomial Naive Bayes
- Database: SQLite
- Frontend: HTML, CSS and small JavaScript enhancements
- Model artifacts: `joblib` files for vectorizer and classifier

### System flow

```text
User pastes message
        ↓
Flask validates and cleans text
        ↓
TF-IDF + Logistic Regression predicts label and probability
        ↓
Influential words + domain status are calculated
        ↓
Result is shown and stored in SQLite history
```

## Phases and Team Allocation

### Phase 1: Planning, dataset and model baseline

**Owner: Person 1 — ML/Data Lead**

- Define labels: `genuine` and `misleading`.
- Gather a public fake-news dataset and document its source/licence.
- Create a small curated set of agriculture and government-scheme messages, with labels and sources.
- Clean duplicates, empty text and inconsistent labels.
- Create stratified train, validation and test splits.
- Train both TF-IDF + Logistic Regression and Naive Bayes.
- Compare accuracy, precision, recall, F1 score and confusion matrix.
- Select the better model and export the vectorizer and classifier.
- Write a short model card with data limitations and evaluation results.

**Deliverable:** `train_model.py`, saved model files, dataset documentation and evaluation report.

### Phase 2: Web application and history log

**Owner: Person 2 — Full-stack/App Lead**

- Create a Flask application with a single clear paste-text form.
- Load the saved model at application start.
- Add a prediction route that returns label, confidence and explanation data.
- Build result cards for likely genuine and likely misleading messages.
- Create SQLite history storage.
- Show recent checks with time, short message preview, label and confidence.
- Add upvote/downvote feedback buttons and store each feedback event.
- Add validation, error messages and safe rendering of pasted text.
- Make the layout responsive for mobile users.

**Database design:**

```sql
checks(
  id, submitted_text, predicted_label, confidence,
  influential_terms, detected_domain, domain_status, created_at
)

feedback(
  id, check_id, vote, created_at
)
```

**Deliverable:** Working local web app with prediction, history and feedback.

### Phase 3: Explainability, domain check and trust layer

**Owner: Person 3 — Explainability/QA Lead**

- Extract the top 3–5 influential input words using TF-IDF values and Logistic Regression coefficients.
- Present terms as words that influenced the model, never as proof of truth.
- Detect URLs in pasted text and safely normalize host names.
- Add a hardcoded verified-portal configuration, for example `gov.in`, `agriwelfare.gov.in` and `pmkisan.gov.in` after source verification.
- Match only exact hosts or legitimate subdomains; reject lookalike addresses such as `pmkisan.gov.in.fake.example`.
- Add clear domain-status language: `verified`, `not in list`, or `no domain found`.
- Write tests for explanation output, domain extraction and lookalike domains.
- Review all result language and add an advisory disclaimer.

**Deliverable:** Explainability utility, verified-domain check, tests and user-facing safety copy.

### Phase 4: Integration, testing and demo readiness

**Owner: Person 2; all three contribute**

- Integrate exported model files with the Flask app.
- Test genuine, misleading, ambiguous, empty, very long and URL-containing messages.
- Verify that every check is saved correctly and feedback is recorded.
- Test mobile layout and ensure colour is not the only indicator of a result.
- Confirm fresh-install instructions work.
- Prepare screenshots, a short demo flow and README instructions.

**Deliverable:** Polished demo-ready MVP and documented setup instructions.

## Shared Interfaces

Person 1 provides a function or service with this response shape:

```json
{
  "label": "likely_misleading",
  "confidence": 87.4,
  "influential_terms": ["urgent", "free", "registration"],
  "model_version": "v1"
}
```

Person 3 adds the following domain result:

```json
{
  "detected_domain": "pmkisan.gov.in",
  "domain_status": "verified"
}
```

Person 2 combines these values, stores them, and displays them in the result view.

## Suggested Four-Day Schedule

| Day | Person 1 | Person 2 | Person 3 | Milestone |
|---|---|---|---|---|
| 1 | Dataset and label rules | Flask/UI skeleton | Domain-list research | Shared contract ready |
| 2 | Train and export baseline model | Prediction form and SQLite history | Keyword/domain utilities | First end-to-end check |
| 3 | Improve dataset and metrics | Feedback and responsive design | Tests and disclaimers | Feature-complete MVP |
| 4 | Validate model examples | Integrate and demo polish | Edge-case review | Final demo and README |

## Definition of Done

- Users can paste a message and receive a prediction in a few seconds.
- The result shows a label, model-confidence percentage and influential terms.
- Detected domains receive an accurate configured-list status.
- Checks and feedback persist in SQLite.
- The model can be reproduced from documented data and a training script.
- The app includes a clear limitation/disclaimer message.
- Core prediction, database and domain-match cases are tested.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Generic fake-news data differs from farm forwards. | Curate a documented agriculture/scheme supplement and evaluate it separately. |
| Users mistake confidence for certainty. | Call it “model confidence” and show a clear advisory disclaimer. |
| Official portal list becomes outdated. | Keep it in a reviewed configuration file with source and last-reviewed date. |
| Small data causes overfitting. | Maintain a held-out test set and use simple, regularized models. |
| Messages contain sensitive personal data. | Do not collect user identities; minimize retained text and offer history clearing if time allows. |

## AI-Agent Execution Guide

This section is written so that you can give each task directly to an AI coding agent. Let one agent act as the **integration owner** (Person 2). Do not let multiple agents edit the same file at the same time.

### 1. Create this project structure first

```text
farm-misinfo-checker/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py                         # Flask application and routes
├── config.py                      # Paths, limits, secret configuration
├── data/
│   ├── raw/                       # Downloaded datasets; do not modify manually
│   ├── processed/                 # Cleaned training CSV files
│   ├── custom_agri_messages.csv    # Curated agriculture examples
│   └── DATASET_CARD.md             # Dataset source, labels, licences, caveats
├── model/
│   ├── classifier.joblib           # Exported Logistic Regression model
│   ├── vectorizer.joblib           # Exported TF-IDF vectorizer
│   └── metrics.json                # Evaluation results and model version
├── scripts/
│   ├── prepare_data.py             # Cleaning and train/test split
│   └── train_model.py              # Train, evaluate and export model
├── services/
│   ├── __init__.py
│   ├── predictor.py                # Model loading, prediction, confidence, keywords
│   ├── domain_check.py             # URL extraction and verified-domain matching
│   └── database.py                 # SQLite initialization and queries
├── config/
│   └── verified_domains.json       # Reviewed government domain allow-list
├── templates/
│   └── index.html                  # Form, result, history and feedback UI
├── static/
│   ├── style.css
│   └── app.js
├── tests/
│   ├── test_predictor.py
│   ├── test_domain_check.py
│   ├── test_database.py
│   └── test_app.py
└── instance/
    └── checker.db                  # Created at runtime; excluded from Git
```

### 2. Decide these conventions before any code is written

Use these fixed values everywhere, so work from separate agents fits together:

| Topic | Agreed convention |
|---|---|
| Python version | Python 3.11 or newer |
| Framework | Flask |
| Model labels | `genuine` and `misleading` internally; user sees “Likely Genuine” and “Likely Misleading” |
| Database | SQLite at `instance/checker.db` |
| Model input limit | 5,000 characters per check |
| Feature output | `label`, `confidence`, `influential_terms`, `detected_domain`, `domain_status` |
| Confidence | Numeric percentage rounded to one decimal; always call it “model confidence” |
| Domain states | `verified`, `not_in_list`, `no_domain_found` |
| Feedback values | `upvote` or `downvote` |
| Git workflow | Every agent works on a separate branch or owns separate files; integration owner merges only after tests pass |

### 3. File-level contracts agents must follow

#### `services/predictor.py`

It must provide this function:

```python
def predict(text: str) -> dict:
    """Return model prediction data for a non-empty text input."""
```

Expected return:

```python
{
    "label": "misleading",
    "confidence": 87.4,
    "influential_terms": ["free", "urgent", "register"],
    "model_version": "v1"
}
```

Rules:

- Load `model/vectorizer.joblib` and `model/classifier.joblib` only once, not for every request.
- Confidence must be derived from `predict_proba` for the returned label.
- Influential terms must come only from words that actually appear in the submitted text.
- If the model files do not exist, raise a clear application error with instructions to run `scripts/train_model.py`.

#### `services/domain_check.py`

It must provide:

```python
def check_domains(text: str) -> dict:
    """Extract the first URL host and return its configured trust-list state."""
```

Expected return:

```python
{
    "detected_domain": "pmkisan.gov.in",
    "domain_status": "verified"
}
```

Rules:

- Read allowed domains from `config/verified_domains.json`.
- A match is valid only when the host equals the approved domain or ends with `.` plus that approved domain.
- Never use a loose substring check; `pmkisan.gov.in.fake-site.com` must be `not_in_list`.
- Return `no_domain_found` when no URL exists.

#### `services/database.py`

It must provide:

```python
def init_db() -> None: ...
def save_check(payload: dict) -> int: ...
def get_recent_checks(limit: int = 20) -> list[dict]: ...
def save_feedback(check_id: int, vote: str) -> None: ...
```

Rules:

- Use parameterized SQL queries only.
- Initialize tables safely if they do not exist.
- Validate feedback values against `upvote` and `downvote`.
- Store timestamps in ISO 8601 UTC format.

#### `app.py`

Required routes:

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Render form and recent history |
| `/check` | POST | Validate text, call prediction/domain services, save and render result |
| `/feedback/<check_id>` | POST | Store an upvote/downvote and return success |
| `/health` | GET | Confirm app, database, and model availability for demo/testing |

Validation rules:

- Reject blank text after trimming whitespace.
- Reject text longer than 5,000 characters.
- Escape user text in the template; never mark it as safe HTML.
- Show errors in the page without exposing internal paths or stack traces.

### 4. Work in this exact order

#### Step A — Integration owner creates the skeleton

Person 2 should first create folders, empty modules, `requirements.txt`, `.gitignore`, and a minimal `README.md`. They should add a placeholder `/health` endpoint and make sure `flask --app app run` starts.

Do **not** build the final UI before the JSON/data contracts above are agreed.

#### Step B — ML agent creates usable model artifacts

Person 1 prepares data and training scripts. The first model must be trained and exported before application integration. If dataset download is difficult, use a small clearly documented starter CSV to complete the pipeline, then replace it with the public data later.

Required model evaluation command:

```text
python scripts/train_model.py
```

It should print evaluation metrics and create all three files in `model/`.

#### Step C — Trust agent builds independently testable utilities

Person 3 builds `domain_check.py`, its JSON configuration, explanation tests, and domain tests without changing `app.py`. Use mocked model/vectorizer objects if Person 1 has not finished exports yet.

#### Step D — App agent connects stable services

Person 2 plugs `predictor.py`, `domain_check.py`, and `database.py` into Flask only after their tests pass. The UI should be usable without JavaScript; JavaScript can improve feedback interactions later.

#### Step E — Team runs end-to-end verification

Run the app locally and manually verify the complete journey. Then run the automated tests:

```text
pytest
```

Resolve integration defects before adding visual polish or optional extras.

### 5. Copy-paste prompts for the AI agents

Give each agent one prompt at a time. Include the project root path in your actual task message.

#### Prompt for Person 1 — ML/data agent

```text
You are the ML/data engineer for a Flask farm-misinformation checker. Work only in data/, scripts/, model/, and tests/test_predictor.py. Do not edit app.py, templates/, static/, or database code.

Build a reproducible TF-IDF + Logistic Regression classifier for labels genuine and misleading. Include Multinomial Naive Bayes as a baseline. Create scripts/prepare_data.py and scripts/train_model.py. The training script must save model/classifier.joblib, model/vectorizer.joblib, and model/metrics.json, and print held-out accuracy, precision, recall, F1, and confusion matrix. Implement services/predictor.py only if it does not conflict with another agent; it must expose predict(text) returning label, one-decimal model confidence, influential terms that occur in input, and model version. Add focused tests. Document data provenance, label rules and limitations in data/DATASET_CARD.md. Do not claim factual verification. Run relevant tests and report every file created/changed plus commands used.
```

#### Prompt for Person 2 — app/integration agent

```text
You are the application and integration engineer for a Flask farm-misinformation checker. Work primarily in app.py, services/database.py, templates/, static/, config.py, requirements.txt, README.md, and tests/test_app.py or tests/test_database.py. Do not modify model training scripts or domain-check logic owned by other agents.

Implement a mobile-friendly Flask app with GET /, POST /check, POST /feedback/<check_id>, and GET /health. Validate trimmed text is non-empty and at most 5000 characters. Call services.predictor.predict(text) and services.domain_check.check_domains(text), save results to SQLite instance/checker.db, show the result and recent checks, and record upvote/downvote feedback. Use parameterized queries, escape displayed user text, and show user-friendly errors. The app must use the agreed service return shapes and still be easy to run with `flask --app app run`. Add tests and update README setup/run instructions. Run tests and report files changed.
```

#### Prompt for Person 3 — trust/explainability agent

```text
You are the trust, explanation, and QA engineer for a Flask farm-misinformation checker. Work only in services/domain_check.py, config/verified_domains.json, tests/test_domain_check.py, tests/test_predictor.py, and documentation sections you own. Do not edit app.py or the frontend.

Implement safe URL extraction and official-domain matching. check_domains(text) must return detected_domain and one of verified, not_in_list, no_domain_found. A verified match is exact host matching or a true subdomain; block lookalikes such as pmkisan.gov.in.fake-site.com. Create a small documented, reviewed list of official government agriculture portals with source and last-reviewed fields. Review predictor explanation behaviour: terms must be based on actual TF-IDF contributions and shown as model influences, not factual evidence. Add unit tests for no URL, valid URL, valid subdomain, case normalization, and lookalike URLs. Report all files changed and test results.
```

### 6. Handoff rules for agents

Each agent must end its work report with these five items:

1. Files created or modified.
2. The exact command used to test the change.
3. Test result or a clear reason it could not run.
4. Public functions/routes added and their expected inputs/outputs.
5. Any integration risk or decision that requires the integration owner’s attention.

The integration owner should inspect the changed-file list before merging. If two agents changed the same file, stop and reconcile the change deliberately; do not blindly accept both versions.

### 7. Final acceptance checklist for the integration owner

- [ ] `python scripts/train_model.py` creates the model files successfully.
- [ ] `flask --app app run` starts without a database/model-loading crash.
- [ ] Empty and over-limit input return a friendly error.
- [ ] A normal text produces label, model confidence, and keyword explanation.
- [ ] A valid configured domain is marked verified.
- [ ] A lookalike domain is not marked verified.
- [ ] The result appears in history after a submission.
- [ ] Upvote/downvote writes one valid feedback record.
- [ ] `pytest` passes.
- [ ] README includes setup, model-training, run, test, data-source, and limitation instructions.
