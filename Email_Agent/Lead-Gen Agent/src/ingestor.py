import pandas as pd
from typing import List
from .models import RawLead

class Ingestor:
    def ingest_csv(self, file_path: str) -> List[RawLead]:
        try:
            df = pd.read_csv(file_path)
            leads = []
            for _, row in df.iterrows():
                leads.append(RawLead(
                    email=row.get('email'),
                    first_name=row.get('first_name'),
                    last_name=row.get('last_name'),
                    company=row.get('company'),
                    source="csv_import"
                ))
            return leads
        except Exception as e:
            print(f"Error ingesting CSV: {e}")
            return []

    def ingest_manual(self, data: List[dict]) -> List[RawLead]:
        return [RawLead(**item, source="manual") for item in data]
