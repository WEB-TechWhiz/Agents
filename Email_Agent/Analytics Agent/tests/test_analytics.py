import pytest
from src.analytics import MetricsEngine
from src.db import Database

@pytest.fixture
def test_engine():
    # Use in-memory SQLite for tests
    db = Database(db_url="sqlite:///:memory:")
    return MetricsEngine(db)

def test_compute_stats(test_engine):
    # Log events
    test_engine.log_event("sent", "test_camp", "lead_1")
    test_engine.log_event("sent", "test_camp", "lead_2")
    test_engine.log_event("open", "test_camp", "lead_1")
    
    stats = test_engine.compute_campaign_stats("test_camp")
    
    assert stats['sent'] == 2
    assert stats['opens'] == 1
    assert stats['open_rate'] == 50.0

def test_anomaly_detection(test_engine):
    # Log 100 sends, 5 opens (5% rate) -> Should trigger anomaly (<10%)
    for i in range(100):
        test_engine.log_event("sent", "anomaly_camp", f"lead_{i}")
        if i < 5:
            test_engine.log_event("open", "anomaly_camp", f"lead_{i}")
            
    anomalies = test_engine.detect_anomalies("anomaly_camp")
    assert len(anomalies) > 0
    assert "Low Open Rate Alert" in anomalies[0]

def test_ab_comparison(test_engine):
    # Camp A: 100% Open
    test_engine.log_event("sent", "camp_a", "lead_1")
    test_engine.log_event("open", "camp_a", "lead_1")
    
    # Camp B: 0% Open
    test_engine.log_event("sent", "camp_b", "lead_2")
    
    comparison = test_engine.compare_variations("camp_a", "camp_b")
    assert comparison['winner'] == "camp_a"
