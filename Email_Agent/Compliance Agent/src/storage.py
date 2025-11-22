import json
import os
from typing import List, Dict
from .models import SuppressionRecord, ConsentRecord

class JsonStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.suppression_file = os.path.join(data_dir, "suppression.json")
        self.consent_file = os.path.join(data_dir, "consent_log.json")
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.suppression_file):
            with open(self.suppression_file, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.consent_file):
            with open(self.consent_file, 'w') as f:
                json.dump([], f)

    def load_suppression_list(self) -> List[Dict]:
        with open(self.suppression_file, 'r') as f:
            return json.load(f)

    def save_suppression_list(self, data: List[Dict]):
        with open(self.suppression_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def load_consent_log(self) -> List[Dict]:
        with open(self.consent_file, 'r') as f:
            return json.load(f)

    def save_consent_log(self, data: List[Dict]):
        with open(self.consent_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
