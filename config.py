import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'checker.db')

# Model configuration
CLASSIFIER_PATH = os.path.join(BASE_DIR, 'model', 'classifier.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.joblib')
METRICS_PATH = os.path.join(BASE_DIR, 'model', 'metrics.json')

# Verified domains configuration
VERIFIED_DOMAINS_PATH = os.path.join(BASE_DIR, 'config', 'verified_domains.json')

# Input limits
MAX_INPUT_LENGTH = 5000
