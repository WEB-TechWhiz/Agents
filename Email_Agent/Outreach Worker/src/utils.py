"""Utility functions for the outreach agent."""

import csv
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def load_contacts_from_csv(csv_file: str) -> List[Dict[str, str]]:
    """
    Load contacts from a CSV file.
    
    Args:
        csv_file: Path to CSV file
        
    Returns:
        List of contact dictionaries
    """
    contacts = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts.append(dict(row))
    return contacts


def save_contacts_to_csv(contacts: List[Dict[str, str]], csv_file: str) -> None:
    """
    Save contacts to a CSV file.
    
    Args:
        contacts: List of contact dictionaries
        csv_file: Path to output CSV file
    """
    if not contacts:
        print("No contacts to save")
        return
    
    fieldnames = contacts[0].keys()
    with open(csv_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    
    print(f"Saved {len(contacts)} contacts to {csv_file}")


def load_json(file_path: str) -> Dict:
    """Load JSON data from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, file_path: str) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def ensure_directory(directory: str) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_log_filename(prefix: str = 'outreach') -> str:
    """
    Generate timestamped log filename.
    
    Args:
        prefix: Filename prefix
        
    Returns:
        Filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.json"


def format_timestamp(iso_string: str) -> str:
    """Format ISO timestamp to readable string."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_string
