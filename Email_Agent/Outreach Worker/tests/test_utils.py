"""Test cases for utils module."""

import unittest
import tempfile
import os
import json
import csv
from pathlib import Path
from src.utils import (
    load_contacts_from_csv,
    save_contacts_to_csv,
    load_json,
    save_json,
    ensure_directory,
    generate_log_filename,
    format_timestamp
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_contacts_from_csv(self):
        """Test loading contacts from CSV file."""
        csv_file = os.path.join(self.temp_dir, 'contacts.csv')
        
        # Create test CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email', 'company'])
            writer.writeheader()
            writer.writerow({'name': 'John', 'email': 'john@test.com', 'company': 'Tech'})
            writer.writerow({'name': 'Jane', 'email': 'jane@test.com', 'company': 'Corp'})
        
        contacts = load_contacts_from_csv(csv_file)
        
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0]['name'], 'John')
        self.assertEqual(contacts[1]['email'], 'jane@test.com')
    
    def test_save_contacts_to_csv(self):
        """Test saving contacts to CSV file."""
        csv_file = os.path.join(self.temp_dir, 'output.csv')
        contacts = [
            {'name': 'Alice', 'email': 'alice@test.com'},
            {'name': 'Bob', 'email': 'bob@test.com'}
        ]
        
        save_contacts_to_csv(contacts, csv_file)
        
        self.assertTrue(os.path.exists(csv_file))
        
        # Verify contents
        loaded = load_contacts_from_csv(csv_file)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]['name'], 'Alice')
    
    def test_save_contacts_empty_list(self):
        """Test saving empty contact list."""
        csv_file = os.path.join(self.temp_dir, 'empty.csv')
        save_contacts_to_csv([], csv_file)
        
        # Should not create file for empty list
        self.assertFalse(os.path.exists(csv_file))
    
    def test_load_json(self):
        """Test loading JSON file."""
        json_file = os.path.join(self.temp_dir, 'test.json')
        test_data = {'key': 'value', 'number': 42}
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        loaded_data = load_json(json_file)
        
        self.assertEqual(loaded_data, test_data)
    
    def test_save_json(self):
        """Test saving JSON file."""
        json_file = os.path.join(self.temp_dir, 'output.json')
        test_data = {'test': 'data', 'list': [1, 2, 3]}
        
        save_json(test_data, json_file)
        
        self.assertTrue(os.path.exists(json_file))
        
        # Verify contents
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded, test_data)
    
    def test_ensure_directory_creates_new(self):
        """Test creating new directory."""
        new_dir = os.path.join(self.temp_dir, 'new_folder')
        
        result = ensure_directory(new_dir)
        
        self.assertTrue(os.path.exists(new_dir))
        self.assertTrue(os.path.isdir(new_dir))
        self.assertIsInstance(result, Path)
    
    def test_ensure_directory_existing(self):
        """Test with existing directory."""
        existing_dir = os.path.join(self.temp_dir, 'existing')
        os.makedirs(existing_dir)
        
        result = ensure_directory(existing_dir)
        
        self.assertTrue(os.path.exists(existing_dir))
        self.assertIsInstance(result, Path)
    
    def test_ensure_directory_nested(self):
        """Test creating nested directories."""
        nested_dir = os.path.join(self.temp_dir, 'level1', 'level2', 'level3')
        
        result = ensure_directory(nested_dir)
        
        self.assertTrue(os.path.exists(nested_dir))
    
    def test_generate_log_filename(self):
        """Test log filename generation."""
        filename = generate_log_filename()
        
        self.assertTrue(filename.startswith('outreach_'))
        self.assertTrue(filename.endswith('.json'))
        self.assertIn('_', filename)
    
    def test_generate_log_filename_custom_prefix(self):
        """Test log filename with custom prefix."""
        filename = generate_log_filename(prefix='campaign')
        
        self.assertTrue(filename.startswith('campaign_'))
        self.assertTrue(filename.endswith('.json'))
    
    def test_format_timestamp_valid(self):
        """Test formatting valid ISO timestamp."""
        iso_string = '2025-01-15T14:30:45'
        result = format_timestamp(iso_string)
        
        self.assertEqual(result, '2025-01-15 14:30:45')
    
    def test_format_timestamp_invalid(self):
        """Test formatting invalid timestamp."""
        invalid_string = 'not-a-timestamp'
        result = format_timestamp(invalid_string)
        
        # Should return original string if parsing fails
        self.assertEqual(result, invalid_string)


if __name__ == '__main__':
    unittest.main()
