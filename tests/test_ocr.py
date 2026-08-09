import sys
import os

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.ocr_service import extract_text_from_image

def test_ocr_none_file():
    result = extract_text_from_image(None)
    assert result["success"] is False
    assert "No file uploaded" in result["message"]

class DummyFile:
    def __init__(self, filename, content=b""):
        self.filename = filename
        self.content = content
    def read(self):
        return self.content

def test_ocr_empty_file():
    dummy = DummyFile("test.png", b"")
    result = extract_text_from_image(dummy)
    assert result["success"] is False
    assert "Empty file" in result["message"]
