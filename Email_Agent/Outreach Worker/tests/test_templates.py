"""Test cases for templates module."""

import unittest
import tempfile
import os
from src.templates import HTMLTemplates


class TestHTMLTemplates(unittest.TestCase):
    """Test cases for HTMLTemplates class."""
    
    def test_professional_template(self):
        """Test professional template generation."""
        title = "Welcome"
        content = "<p>This is test content</p>"
        footer = "Contact us"
        
        result = HTMLTemplates.professional_template(title, content, footer)
        
        self.assertIn(title, result)
        self.assertIn(content, result)
        self.assertIn(footer, result)
        self.assertIn('<!DOCTYPE html>', result)
        self.assertIn('gradient', result)  # Check for styling
    
    def test_professional_template_no_footer(self):
        """Test professional template without custom footer."""
        result = HTMLTemplates.professional_template("Title", "Content")
        
        self.assertIn("© 2025", result)  # Default footer
    
    def test_simple_template(self):
        """Test simple template generation."""
        content = "<h1>Hello World</h1>"
        
        result = HTMLTemplates.simple_template(content)
        
        self.assertIn(content, result)
        self.assertIn('<!DOCTYPE html>', result)
        self.assertIn('container', result)
    
    def test_minimal_template(self):
        """Test minimal template generation."""
        content = "<p>Minimal content</p>"
        
        result = HTMLTemplates.minimal_template(content)
        
        self.assertIn(content, result)
        self.assertIn('<!DOCTYPE html>', result)
    
    def test_load_from_file(self):
        """Test loading template from file."""
        # Create temporary template file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write('<html><body>Hello $name from $company</body></html>')
            temp_file = f.name
        
        try:
            result = HTMLTemplates.load_from_file(
                temp_file,
                name="John",
                company="Tech Corp"
            )
            
            self.assertIn("John", result)
            self.assertIn("Tech Corp", result)
            self.assertNotIn("$name", result)
        finally:
            os.unlink(temp_file)
    
    def test_load_from_file_missing_variables(self):
        """Test loading template with missing variables."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write('<html><body>Hello $name from $company</body></html>')
            temp_file = f.name
        
        try:
            result = HTMLTemplates.load_from_file(
                temp_file,
                name="John"
                # company is missing
            )
            
            self.assertIn("John", result)
            self.assertIn("$company", result)  # Should remain as placeholder
        finally:
            os.unlink(temp_file)
    
    def test_load_from_file_not_found(self):
        """Test loading non-existent template file."""
        with self.assertRaises(FileNotFoundError):
            HTMLTemplates.load_from_file('nonexistent_file.html')
    
    def test_templates_are_valid_html(self):
        """Test that all templates produce valid HTML structure."""
        templates = [
            HTMLTemplates.professional_template("Title", "Content"),
            HTMLTemplates.simple_template("Content"),
            HTMLTemplates.minimal_template("Content")
        ]
        
        for template in templates:
            with self.subTest(template=template[:50]):
                self.assertIn('<!DOCTYPE html>', template)
                self.assertIn('<html>', template)
                self.assertIn('</html>', template)
                self.assertIn('<body', template)
                self.assertIn('</body>', template)


if __name__ == '__main__':
    unittest.main()
