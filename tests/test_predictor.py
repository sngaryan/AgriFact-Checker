import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import services.predictor as predictor

def test_predict_empty_text():
    with pytest.raises(ValueError):
        predictor.predict("")
        
    with pytest.raises(ValueError):
        predictor.predict("   ")

@patch("services.predictor._classifier")
@patch("services.predictor._vectorizer")
@patch("services.predictor.load_model")
def test_predict_success(mock_load_model, mock_vectorizer, mock_classifier):
    # Setup mock vectorizer vocabulary
    mock_vocab = {"free": 0, "scheme": 1, "urgent": 2}
    mock_vectorizer.vocabulary_ = mock_vocab
    mock_vectorizer.get_feature_names_out.return_value = np.array(["free", "scheme", "urgent"])
    
    # Mock TF-IDF transform output. We want TF-IDF value to be > 0 for words in text.
    mock_tfidf = MagicMock()
    # mock_tfidf[0, idx] returning values for free (0) and scheme (1)
    mock_tfidf.__getitem__.side_effect = lambda idx: 0.8 if idx[1] in (0, 1) else 0.0
    mock_vectorizer.transform.return_value = mock_tfidf
    
    # Setup mock classifier classes and predict outputs
    mock_classifier.classes_ = ["genuine", "misleading"]
    mock_classifier.predict.return_value = np.array([1]) # Index 1 corresponds to "misleading"
    mock_classifier.predict_proba.return_value = np.array([[0.126, 0.874]]) # 87.4% confidence
    
    # Coefficients: positive values for class 1 (misleading)
    # Shape is (1, n_features)
    mock_classifier.coef_ = np.array([[1.5, 0.5, -0.8]])
    
    res = predictor.predict("This is a free scheme forward")
    
    assert res["label"] == "misleading"
    assert res["confidence"] == 87.4
    assert "free" in res["influential_terms"]
    assert "scheme" in res["influential_terms"]
    assert res["model_version"] == "v1"
