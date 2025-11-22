from src.db import Database
from src.analytics import MetricsEngine
import random

def main():
    db = Database()
    engine = MetricsEngine(db)
    
    print("--- Analytics Agent Started ---")
    
    # 1. Simulate Data for Campaign A (Good Performance)
    print("\nSimulating Campaign A (Good)...")
    for i in range(100):
        engine.log_event("sent", "camp_a", f"lead_{i}")
        if i < 25: # 25% Open Rate
            engine.log_event("open", "camp_a", f"lead_{i}")
        if i < 5:  # 5% Click Rate
            engine.log_event("click", "camp_a", f"lead_{i}")

    stats_a = engine.compute_campaign_stats("camp_a")
    print(f"Campaign A Stats: {stats_a}")
    
    # 2. Simulate Campaign B (Bad Performance - Anomaly)
    print("\nSimulating Campaign B (Bad)...")
    for i in range(100):
        engine.log_event("sent", "camp_b", f"lead_{i}")
        if i < 5: # 5% Open Rate (Below 10% threshold)
            engine.log_event("open", "camp_b", f"lead_{i}")

    stats_b = engine.compute_campaign_stats("camp_b")
    print(f"Campaign B Stats: {stats_b}")
    
    # 3. Detect Anomalies
    print("\nChecking Anomalies...")
    anomalies_a = engine.detect_anomalies("camp_a")
    anomalies_b = engine.detect_anomalies("camp_b")
    
    if anomalies_a: print(f"Campaign A Anomalies: {anomalies_a}")
    else: print("Campaign A: No anomalies.")
        
    if anomalies_b: print(f"Campaign B Anomalies: {anomalies_b}")
    else: print("Campaign B: No anomalies.")
    
    # 4. A/B Test Comparison
    print("\nComparing A vs B...")
    comparison = engine.compare_variations("camp_a", "camp_b")
    print(f"Winner: {comparison['winner']} (Metric: {comparison['metric']})")

if __name__ == "__main__":
    main()
