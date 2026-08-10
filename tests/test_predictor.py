import os
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import services.predictor as predictor

def test_predict_empty_text():
    """Verify that empty or whitespace-only inputs raise ValueError."""
    with pytest.raises(ValueError):
        predictor.predict("")
        
    with pytest.raises(ValueError):
        predictor.predict("   ")

@patch("services.predictor._classifier")
@patch("services.predictor._vectorizer")
@patch("services.predictor.load_model")
def test_predict_mock_success(mock_load_model, mock_vectorizer, mock_classifier):
    """Test predictor with mocked classifier and vectorizer."""
    mock_vocab = {"free": 0, "scheme": 1, "urgent": 2}
    mock_vectorizer.vocabulary_ = mock_vocab
    mock_vectorizer.get_feature_names_out.return_value = np.array(["free", "scheme", "urgent"])
    
    mock_tfidf = MagicMock()
    mock_tfidf.__getitem__.side_effect = lambda idx: 0.8 if idx[1] in (0, 1) else 0.0
    mock_vectorizer.transform.return_value = mock_tfidf
    
    mock_classifier.classes_ = np.array(["genuine", "misleading"])
    mock_classifier.predict.return_value = np.array([1])  # Index 1 = misleading
    mock_classifier.predict_proba.return_value = np.array([[0.126, 0.874]])
    mock_classifier.coef_ = np.array([[1.5, 0.5, -0.8]])
    
    res = predictor.predict("This is a free scheme forward")
    
    assert res["label"] == "misleading"
    assert res["confidence"] > 80.0
    assert "free" in res["influential_terms"]
    assert "scheme" in res["influential_terms"]
    assert res["model_version"] == "v1"

def test_predict_real_model_genuine():
    """Integration test predicting a genuine agricultural scheme statement with trained model."""
    text = "Under PM-KISAN scheme eligible farmers receive Rs 6000 per year directly in bank accounts. Check details on pmkisan.gov.in."
    res = predictor.predict(text)
    
    assert "label" in res
    assert res["label"] in ["genuine", "misleading"]
    assert isinstance(res["confidence"], float)
    assert 0.0 <= res["confidence"] <= 100.0
    assert isinstance(res["influential_terms"], list)
    assert len(res["influential_terms"]) <= 5
    assert res["model_version"] == "v1"

def test_predict_real_model_misleading():
    """Integration test predicting a fake scam message with trained model."""
    text = "Urgent: Get 90% tractor subsidy immediately by filling Aadhaar form at http://pmkisan-tractor-subsidy.online!"
    res = predictor.predict(text)
    
    assert res["label"] == "misleading"
    assert res["confidence"] > 50.0
    assert isinstance(res["influential_terms"], list)
    # Ensure influential terms are words present in input
    for term in res["influential_terms"]:
        assert term.lower() in text.lower()

def test_predict_missing_model_raises_error():
    """Test that missing model files raise FileNotFoundError with instructions."""
    predictor._classifier = None
    predictor._vectorizer = None
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError) as exc_info:
            predictor.predict("Some agriculture sample text")
        assert "train_model.py" in str(exc_info.value)
