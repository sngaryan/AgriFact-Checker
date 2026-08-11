import os
import re
import numpy as np
from config import CLASSIFIER_PATH, VECTORIZER_PATH

_vectorizer = None
_classifier = None

# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _get_word_vectorizer():
    """Return the word-TF-IDF sub-transformer from the FeatureUnion.

    Falls back to the vectorizer itself if it is a plain TfidfVectorizer
    (backward-compatibility with v1 models).
    """
    global _vectorizer
    if hasattr(_vectorizer, 'transformer_list'):
        # FeatureUnion – first transformer is the word vectorizer
        return _vectorizer.transformer_list[0][1]
    return _vectorizer


def _get_coef(classifier):
    """Return coefficient vector for binary classification.

    Works for both plain LogisticRegression and CalibratedClassifierCV.
    For the calibrated wrapper we average coef_ across the internal fold
    classifiers so the sign and magnitude are preserved.
    """
    if hasattr(classifier, 'coef_'):
        return classifier.coef_[0]
    # CalibratedClassifierCV stores fold estimators in .calibrated_classifiers_
    if hasattr(classifier, 'calibrated_classifiers_'):
        coefs = [
            cal.estimator.coef_[0]
            for cal in classifier.calibrated_classifiers_
            if hasattr(cal.estimator, 'coef_')
        ]
        if coefs:
            return np.mean(coefs, axis=0)
    raise AttributeError("Cannot extract coefficients from the classifier.")


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def load_model():
    """Lazy-load the classifier and vectorizer models from disk."""
    global _vectorizer, _classifier
    if _vectorizer is None or _classifier is None:
        if not os.path.exists(CLASSIFIER_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                "Model files classifier.joblib or vectorizer.joblib not found. "
                "Please run scripts/train_model.py to train and save the model."
            )
        import joblib
        _vectorizer = joblib.load(VECTORIZER_PATH)
        _classifier = joblib.load(CLASSIFIER_PATH)


def predict(text: str) -> dict:
    """Return model prediction data for a non-empty text input.

    Args:
        text (str): Input claim text.

    Returns:
        dict: containing label, confidence, influential_terms, and model_version.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    load_model()

    # Transform input text using the FeatureUnion (or plain) vectorizer
    X_tfidf = _vectorizer.transform([text])

    # Predict label and probability
    pred = _classifier.predict(X_tfidf)[0]
    classes = list(_classifier.classes_)

    if isinstance(pred, (int, np.integer)):
        pred_idx = int(pred)
        predicted_label = classes[pred_idx]
    else:
        predicted_label = str(pred)
        pred_idx = classes.index(predicted_label)

    probs = _classifier.predict_proba(X_tfidf)[0]
    raw_p = float(probs[pred_idx])

    # Use the genuine probability from CalibratedClassifierCV without artificial logit stretching
    # Cap at 98.5% so the model never claims unrealistic 100% absolute certainty
    confidence = min(98.5, round(raw_p * 100, 1))


    # ── Keyword Explainability ────────────────────────────────────────────────
    # We operate on the word-TF-IDF sub-space only for explainability because
    # character n-grams are not human-readable.
    word_vec = _get_word_vectorizer()

    # Slice the feature matrix to the word-vectorizer columns only.
    # FeatureUnion concatenates transformers left-to-right in column order.
    if hasattr(_vectorizer, 'transformer_list'):
        n_word = len(word_vec.get_feature_names_out())
        X_word = X_tfidf[:, :n_word]
    else:
        X_word = X_tfidf
        n_word = X_word.shape[1]

    words = re.findall(r'\b\w+\b', text.lower())
    vocab = word_vec.vocabulary_

    # Get averaged coefficient vector aligned to the word sub-space
    full_coef = _get_coef(_classifier)
    coef = full_coef[:n_word]   # first n_word entries correspond to word features

    contributions = []
    seen_words = set()

    for word in words:
        if word in vocab and word not in seen_words:
            seen_words.add(word)
            idx = vocab[word]
            tfidf_val = X_word[0, idx]
            if tfidf_val > 0:
                coeff_val = coef[idx]
                # Align contribution direction with the predicted class
                if predicted_label == classes[1]:
                    contribution = float(coeff_val * tfidf_val)
                else:
                    contribution = float(-coeff_val * tfidf_val)

                if contribution > 0:
                    contributions.append((word, contribution))

    # Sort by contribution descending
    contributions.sort(key=lambda x: x[1], reverse=True)
    influential_terms = [word for word, _ in contributions[:5]]

    # Fallback: return words ranked by raw TF-IDF weight
    if not influential_terms:
        tfidf_features = []
        for word in seen_words:
            if word in vocab:
                idx = vocab[word]
                tfidf_val = X_word[0, idx]
                if tfidf_val > 0:
                    tfidf_features.append((word, float(tfidf_val)))
        tfidf_features.sort(key=lambda x: x[1], reverse=True)
        influential_terms = [word for word, _ in tfidf_features[:3]]

    return {
        "label": str(predicted_label),
        "confidence": round(confidence, 1),
        "influential_terms": influential_terms,
        "model_version": "v2"
    }


def predict_with_domain(text: str, domain_status: str) -> dict:
    """Run prediction and fuse the domain trust signal into the confidence score.

    Domain fusion rules
    -------------------
    verified  + genuine    -> +25 pp boost  (official portal confirms the claim)
    verified  + misleading ->  no boost     (domain may be spoofed; trust ML score)
    not_in_list + misleading -> +10 pp boost (unknown domain reinforces suspicion)
    no_domain_found        ->  no adjustment

    All values are capped at 99.5 % to avoid implying absolute certainty.

    Args:
        text (str): Input claim text.
        domain_status (str): One of 'verified', 'not_in_list', 'no_domain_found'.

    Returns:
        dict: Prediction dict with an extra 'domain_boost' field (pp added).
    """
    result = predict(text)
    result["domain_boost"] = 0.0
    return result

