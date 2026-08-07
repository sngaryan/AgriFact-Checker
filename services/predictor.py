import os
import re
import numpy as np
from config import CLASSIFIER_PATH, VECTORIZER_PATH

_vectorizer = None
_classifier = None

def load_model():
    """Lazy load the classifier and vectorizer models."""
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
    
    # Preprocess/tokenize similarly to vectorizer requirements
    # Transform input text
    X_tfidf = _vectorizer.transform([text])
    
    # Predict label and probability
    pred_idx = _classifier.predict(X_tfidf)[0]
    labels = _classifier.classes_
    predicted_label = labels[pred_idx]
    
    probs = _classifier.predict_proba(X_tfidf)[0]
    confidence = float(probs[pred_idx]) * 100
    
    # Extract influential terms:
    # 1. Tokenize words in input text
    # 2. Match them to vocabulary indices
    # 3. Compute contribution = TFIDF value * Coefficient
    # 4. Sort and return top 3-5 words
    
    words = re.findall(r'\b\w+\b', text.lower())
    feature_names = _vectorizer.get_feature_names_out()
    vocab = _vectorizer.vocabulary_
    
    # Get Logistic Regression coefficients for the predicted class
    # For binary classification with LogisticRegression, coef_ has shape (1, n_features)
    # The coefficient is for classes_[1] (usually misleading if labeled alphabetically/numerically)
    # If binary, coef_ represents the log odds of class 1.
    coef = _classifier.coef_[0]
    
    contributions = []
    seen_words = set()
    
    for word in words:
        if word in vocab and word not in seen_words:
            seen_words.add(word)
            idx = vocab[word]
            tfidf_val = X_tfidf[0, idx]
            if tfidf_val > 0:
                # If predicted label is class 1, positive coefficient means it contributes to class 1.
                # If predicted label is class 0, negative coefficient means it contributes to class 0.
                # Let's check which class class_idx corresponds to.
                # We want absolute weight or positive/negative alignment.
                # To be general: coefficient * tfidf.
                # If predicted class is classes_[1], positive contribution means positive coef.
                # If predicted class is classes_[0], positive contribution means negative coef.
                coeff_val = coef[idx]
                if predicted_label == labels[1]:
                    contribution = coeff_val * tfidf_val
                else:
                    contribution = -coeff_val * tfidf_val
                
                # We only want terms that positively influence this prediction
                if contribution > 0:
                    contributions.append((word, contribution))
                    
    # Sort by contribution descending
    contributions.sort(key=lambda x: x[1], reverse=True)
    influential_terms = [word for word, _ in contributions[:5]]
    
    # Fallback to general tfidf features if no positive contribution terms are found
    if not influential_terms:
        # Just return words in text sorted by their TFIDF value
        tfidf_features = []
        for word in seen_words:
            idx = vocab[word]
            tfidf_val = X_tfidf[0, idx]
            if tfidf_val > 0:
                tfidf_features.append((word, tfidf_val))
        tfidf_features.sort(key=lambda x: x[1], reverse=True)
        influential_terms = [word for word, _ in tfidf_features[:3]]
        
    return {
        "label": str(predicted_label),
        "confidence": round(confidence, 1),
        "influential_terms": influential_terms,
        "model_version": "v1"
    }
