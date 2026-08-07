import os
import tempfile
import pytest
from unittest.mock import patch
import config

from services.database import init_db
import app as flask_app

@pytest.fixture(scope="module", autouse=True)
def setup_app_db():
    original_path = config.DATABASE_PATH
    app_db_fd, temp_app_db_path = tempfile.mkstemp()
    os.close(app_db_fd)
    config.DATABASE_PATH = temp_app_db_path
    
    init_db()
    yield
    
    config.DATABASE_PATH = original_path
    if os.path.exists(temp_app_db_path):
        try:
            os.unlink(temp_app_db_path)
        except Exception:
            pass

@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client

def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert "database" in data
    assert "model" in data

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Verify advisory or scheme" in response.data

def test_check_validation_empty(client):
    response = client.post("/check", data={"text": ""})
    assert response.status_code == 200
    assert b"Please enter some text to check." in response.data

def test_check_validation_too_long(client):
    response = client.post("/check", data={"text": "a" * (config.MAX_INPUT_LENGTH + 1)})
    assert response.status_code == 200
    assert b"Text exceeds the limit" in response.data

@patch("app.predict")
@patch("app.check_domains")
def test_check_success(mock_check_domains, mock_predict, client):
    mock_predict.return_value = {
        "label": "genuine",
        "confidence": 92.4,
        "influential_terms": ["official", "scheme"],
        "model_version": "v1"
    }
    mock_check_domains.return_value = {
        "detected_domain": "pmkisan.gov.in",
        "domain_status": "verified"
    }
    
    response = client.post("/check", data={"text": "Verify this official message from pmkisan.gov.in"})
    assert response.status_code == 200
    assert b"Likely Genuine" in response.data
    assert b"92.4%" in response.data
    assert b"Verified Portal: pmkisan.gov.in" in response.data

@patch("app.predict")
@patch("app.check_domains")
def test_check_model_not_trained(mock_check_domains, mock_predict, client):
    mock_predict.side_effect = FileNotFoundError("Model files not found")
    mock_check_domains.return_value = {
        "detected_domain": "",
        "domain_status": "no_domain_found"
    }
    
    response = client.post("/check", data={"text": "Verify this simple message"})
    assert response.status_code == 200
    assert b"The classification model has not been trained yet" in response.data
