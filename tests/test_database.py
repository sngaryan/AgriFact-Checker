import os
import tempfile
import pytest
import config

from services.database import init_db, save_check, get_recent_checks, save_feedback

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    original_path = config.DATABASE_PATH
    db_fd, temp_db_path = tempfile.mkstemp()
    os.close(db_fd)
    config.DATABASE_PATH = temp_db_path
    
    init_db()
    yield
    
    config.DATABASE_PATH = original_path
    if os.path.exists(temp_db_path):
        try:
            os.unlink(temp_db_path)
        except Exception:
            pass

def test_database_operations():
    # 1. Verify table initialization does not crash
    init_db()
    
    # 2. Test saving a check
    payload = {
        "submitted_text": "Sample agriculture forwarding message about PM-Kisan scheme.",
        "predicted_label": "genuine",
        "confidence": 95.5,
        "influential_terms": ["PM-Kisan", "scheme"],
        "detected_domain": "pmkisan.gov.in",
        "domain_status": "verified"
    }
    
    check_id = save_check(payload)
    assert check_id > 0
    
    # 3. Test retrieving recent checks
    recent = get_recent_checks(limit=5)
    assert len(recent) == 1
    assert recent[0]["id"] == check_id
    assert recent[0]["submitted_text"] == payload["submitted_text"]
    assert recent[0]["predicted_label"] == payload["predicted_label"]
    assert recent[0]["confidence"] == payload["confidence"]
    assert recent[0]["influential_terms"] == payload["influential_terms"]
    assert recent[0]["detected_domain"] == payload["detected_domain"]
    assert recent[0]["domain_status"] == payload["domain_status"]
    assert "created_at" in recent[0]
    
    # 4. Test saving feedback
    save_feedback(check_id, "upvote")
    save_feedback(check_id, "downvote")
    
    # 5. Test invalid feedback validation
    with pytest.raises(ValueError):
        save_feedback(check_id, "invalid_vote")
        
    with pytest.raises(ValueError):
        save_feedback(999999, "upvote") # non-existent check_id
