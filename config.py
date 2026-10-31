import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Security configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(BASE_DIR, 'instance', 'checker.db'))

# Model configuration
CLASSIFIER_PATH = os.getenv('MODEL_PATH', os.path.join(BASE_DIR, 'model', 'classifier.joblib'))
VECTORIZER_PATH = os.getenv('VECTORIZER_PATH', os.path.join(BASE_DIR, 'model', 'vectorizer.joblib'))
METRICS_PATH = os.getenv('METRICS_PATH', os.path.join(BASE_DIR, 'model', 'metrics.json'))

# Verified domains configuration
VERIFIED_DOMAINS_PATH = os.getenv('VERIFIED_DOMAINS_PATH', os.path.join(BASE_DIR, 'config', 'verified_domains.json'))

# Input limits
MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH', '5000'))
