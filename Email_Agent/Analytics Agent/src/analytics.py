import pandas as pd
from sqlalchemy.orm import Session
from .models import Event, CampaignMetrics
from .db import Database
from datetime import datetime, timedelta

class MetricsEngine:
    def __init__(self, db: Database):
        self.db = db

    def log_event(self, event_type: str, campaign_id: str, lead_id: str, details: str = None):
        session = self.db.get_session()
        event = Event(
            event_type=event_type,
            campaign_id=campaign_id,
            lead_id=lead_id,
            details=details
        )
        session.add(event)
        session.commit()
        session.close()

    def compute_campaign_stats(self, campaign_id: str) -> dict:
        session = self.db.get_session()
        events = session.query(Event).filter_by(campaign_id=campaign_id).all()
        session.close()

        if not events:
            return {}

        df = pd.DataFrame([{
            'event_type': e.event_type,
            'timestamp': e.timestamp,
            'lead_id': e.lead_id
        } for e in events])

        sent = df[df['event_type'] == 'sent'].shape[0]
        opens = df[df['event_type'] == 'open'].shape[0]
        clicks = df[df['event_type'] == 'click'].shape[0]
        replies = df[df['event_type'] == 'reply'].shape[0]

        open_rate = (opens / sent * 100) if sent > 0 else 0
        click_rate = (clicks / sent * 100) if sent > 0 else 0
        reply_rate = (replies / sent * 100) if sent > 0 else 0

        return {
            "campaign_id": campaign_id,
            "sent": sent,
            "opens": opens,
            "clicks": clicks,
            "replies": replies,
            "open_rate": round(open_rate, 2),
            "click_rate": round(click_rate, 2),
            "reply_rate": round(reply_rate, 2)
        }

    def detect_anomalies(self, campaign_id: str) -> list:
        """
        Detects if open rate drops significantly compared to recent average.
        Simple implementation: Checks if open rate < 10% (hard threshold for demo).
        """
        stats = self.compute_campaign_stats(campaign_id)
        anomalies = []
        
        if stats.get('sent', 0) > 10: # Only check if significant volume
            if stats['open_rate'] < 10.0:
                anomalies.append(f"Low Open Rate Alert: {stats['open_rate']}% (Threshold: 10%)")
            
        return anomalies

    def compare_variations(self, campaign_a: str, campaign_b: str) -> dict:
        stats_a = self.compute_campaign_stats(campaign_a)
        stats_b = self.compute_campaign_stats(campaign_b)
        
        winner = None
        if stats_a.get('open_rate', 0) > stats_b.get('open_rate', 0):
            winner = campaign_a
        elif stats_b.get('open_rate', 0) > stats_a.get('open_rate', 0):
            winner = campaign_b
            
        return {
            "campaign_a": stats_a,
            "campaign_b": stats_b,
            "winner": winner,
            "metric": "open_rate"
        }
