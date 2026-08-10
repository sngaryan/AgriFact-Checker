import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from config import CLASSIFIER_PATH, VECTORIZER_PATH, METRICS_PATH

PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def evaluate_model(model, X_test, y_test, model_name="Model", labels=None):
    """Evaluate a trained model and return a metrics dictionary."""
    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    
    # Binary metrics for 'misleading' class
    pos_label = 'misleading'
    precision_bin, recall_bin, f1_bin, _ = precision_recall_fscore_support(
        y_test, y_pred, pos_label=pos_label, average='binary', zero_division=0
    )
    
    # Macro metrics across all classes
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_test, y_pred, average='macro', zero_division=0
    )
    
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    
    return {
        "model_name": model_name,
        "accuracy": round(acc, 4),
        "precision_misleading": round(float(precision_bin), 4),
        "recall_misleading": round(float(recall_bin), 4),
        "f1_misleading": round(float(f1_bin), 4),
        "precision_macro": round(float(precision_macro), 4),
        "recall_macro": round(float(recall_macro), 4),
        "f1_macro": round(float(f1_macro), 4),
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_labels": list(labels)
    }

def train_and_evaluate():
    """Train TF-IDF + Logistic Regression and Naive Bayes baseline, compare, and save artifacts."""
    train_path = os.path.join(PROCESSED_DIR, 'train.csv')
    val_path = os.path.join(PROCESSED_DIR, 'val.csv')
    test_path = os.path.join(PROCESSED_DIR, 'test.csv')
    
    if not (os.path.exists(train_path) and os.path.exists(test_path)):
        raise FileNotFoundError("Processed datasets not found. Please run scripts/prepare_data.py first.")
        
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)
    
    print(f"Dataset splits loaded:")
    print(f"  Train: {len(train_df)} samples")
    print(f"  Val:   {len(val_df)} samples")
    print(f"  Test:  {len(test_df)} samples")
    
    # FeatureUnion of word n-grams + character subword n-grams.
    # The char_wb analyser tokenizes within word boundaries, so it captures
    # partial scheme names, transliterated Hindi words, and typos that would
    # otherwise produce an all-zero TF-IDF vector (leading to 50 % confidence).
    vectorizer = FeatureUnion([
        ('word', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=3000,
            stop_words='english',
            sublinear_tf=True
        )),
        ('char', TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(3, 5),
            max_features=5000,
            sublinear_tf=True
        ))
    ])
    
    # Combine train + val for training text, test for evaluation
    X_train_text = train_df['text'].tolist()
    y_train = train_df['label'].tolist()
    
    X_val_text = val_df['text'].tolist()
    y_val = val_df['label'].tolist()
    
    X_test_text = test_df['text'].tolist()
    y_test = test_df['label'].tolist()
    
    # Fit vectorizer on training text
    X_train = vectorizer.fit_transform(X_train_text)
    X_val = vectorizer.transform(X_val_text)
    X_test = vectorizer.transform(X_test_text)
    
    labels = np.unique(y_train)
    
    print("\n--- Training Model 1: Calibrated Logistic Regression ---")
    # CalibratedClassifierCV wraps Logistic Regression with Platt scaling (sigmoid)
    # so that predict_proba() returns well-spread probabilities (70-99%) instead of
    # collapsing near 50% on in-distribution data. We use a higher C=5.0 to give
    # the base classifier more freedom before calibration smooths it out.
    # cv=3 is chosen to accommodate the small dataset size (56 training samples).
    base_lr = LogisticRegression(C=5.0, max_iter=1000, random_state=42)
    log_reg = CalibratedClassifierCV(estimator=base_lr, method='sigmoid', cv=3)
    log_reg.fit(X_train, y_train)
    lr_val_metrics = evaluate_model(log_reg, X_val, y_val, "Calibrated Logistic Regression (Val)", labels)
    lr_test_metrics = evaluate_model(log_reg, X_test, y_test, "Calibrated Logistic Regression (Test)", labels)
    
    print("\n--- Training Model 2: Multinomial Naive Bayes Baseline ---")
    nb = MultinomialNB(alpha=0.5)
    nb.fit(X_train, y_train)
    nb_val_metrics = evaluate_model(nb, X_val, y_val, "Multinomial Naive Bayes (Val)", labels)
    nb_test_metrics = evaluate_model(nb, X_test, y_test, "Multinomial Naive Bayes (Test)", labels)
    
    print("\n" + "="*70)
    print("MODEL EVALUATION COMPARISON (HELD-OUT TEST SET)")
    print("="*70)
    print(f"{'Metric':<25} | {'Logistic Regression':<20} | {'Naive Bayes Baseline':<20}")
    print("-" * 70)
    print(f"{'Accuracy':<25} | {lr_test_metrics['accuracy']:<20} | {nb_test_metrics['accuracy']:<20}")
    print(f"{'Precision (Misleading)':<25} | {lr_test_metrics['precision_misleading']:<20} | {nb_test_metrics['precision_misleading']:<20}")
    print(f"{'Recall (Misleading)':<25} | {lr_test_metrics['recall_misleading']:<20} | {nb_test_metrics['recall_misleading']:<20}")
    print(f"{'F1 Score (Misleading)':<25} | {lr_test_metrics['f1_misleading']:<20} | {nb_test_metrics['f1_misleading']:<20}")
    print(f"{'F1 Score (Macro)':<25} | {lr_test_metrics['f1_macro']:<20} | {nb_test_metrics['f1_macro']:<20}")
    print("="*70)
    print("Confusion Matrix (Logistic Regression):")
    print(f"  Labels: {labels}")
    print(f"  Matrix: {lr_test_metrics['confusion_matrix']}")
    print("="*70)
    
    # We select the Calibrated Logistic Regression as the primary model.
    # The underlying LR coefficients are still accessible via log_reg.calibrated_classifiers_
    # for keyword explainability (see services/predictor.py).
    selected_classifier = log_reg
    selected_name = "Calibrated Logistic Regression (TF-IDF + Char N-gram)"
    
    # Save artifacts
    os.makedirs(os.path.dirname(CLASSIFIER_PATH), exist_ok=True)
    joblib.dump(selected_classifier, CLASSIFIER_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"\nModel exported successfully to:")
    print(f"  - Classifier: {CLASSIFIER_PATH}")
    print(f"  - Vectorizer: {VECTORIZER_PATH}")
    
    # Metrics report output
    word_features = len(vectorizer.transformer_list[0][1].get_feature_names_out())
    char_features = len(vectorizer.transformer_list[1][1].get_feature_names_out())
    metrics_data = {
        "model_version": "v2",
        "selected_model": selected_name,
        "test_metrics": lr_test_metrics,
        "val_metrics": lr_val_metrics,
        "baseline_naive_bayes_test": nb_test_metrics,
        "train_samples": len(train_df),
        "val_samples": len(val_df),
        "test_samples": len(test_df),
        "feature_count": word_features + char_features,
        "word_features": word_features,
        "char_features": char_features,
        "classes": list(labels),
        "improvements": [
            "FeatureUnion: word bigrams + char 3-5-grams eliminates OOV zero vectors",
            "CalibratedClassifierCV (Platt sigmoid) produces well-spread confidence scores",
            "C=5.0 reduces regularization bias on small agriculture dataset"
        ]
    }
    
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics_data, f, indent=2)
    print(f"  - Metrics JSON: {METRICS_PATH}")
    
    return metrics_data

if __name__ == '__main__':
    train_and_evaluate()
