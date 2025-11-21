"""Configuration settings for the outreach agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
ATTACHMENTS_DIR = BASE_DIR / 'attachments'
TEMPLATES_DIR = BASE_DIR / 'templates'

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'gmail')

# Campaign settings
DEFAULT_DELAY = float(os.getenv('DEFAULT_DELAY', '2.0'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '5'))

# Logging
LOG_ENABLED = os.getenv('LOG_ENABLED', 'true').lower() == 'true'
LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')  # json or csv

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, ATTACHMENTS_DIR]:
    directory.mkdir(exist_ok=True)

