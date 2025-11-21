"""Test cases for validators module."""

import unittest
from src.validators import EmailValidator, ContactValidator


class TestEmailValidator(unittest.TestCase):
    """Test cases for EmailValidator class."""
    
    def test_validate_email_valid(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "first+last@company.org",
            "admin@subdomain.example.com",
            "123@numbers.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(EmailValidator.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            "",
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com",
            "user@.com",
            "user@domain",
            None,
            123
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(EmailValidator.validate_email(email))
    
    def test_validate_email_with_whitespace(self):
        """Test email validation with leading/trailing whitespace."""
        self.assertTrue(EmailValidator.validate_email("  test@example.com  "))
    
    def test_clean_email(self):
        """Test email cleaning and normalization."""
        self.assertEqual(EmailValidator.clean_email("  Test@Example.COM  "), "test@example.com")
        self.assertEqual(EmailValidator.clean_email(""), "")
        self.assertEqual(EmailValidator.clean_email(None), "")
    
    def test_validate_contacts(self):
        """Test batch contact validation."""
        contacts = [
            {"name": "John", "email": "john@example.com"},
            {"name": "Jane", "email": "invalid-email"},
            {"name": "Bob", "email": "bob@test.com"}
        ]
        
        valid, invalid = EmailValidator.validate_contacts(contacts)
        
        self.assertEqual(len(valid), 2)
        self.assertEqual(len(invalid), 1)
        self.assertEqual(invalid[0]['email'], "invalid-email")
        self.assertIn('validation_error', invalid[0])


class TestContactValidator(unittest.TestCase):
    """Test cases for ContactValidator class."""
    
    def test_validate_contact_valid(self):
        """Test validation of valid contact."""
        contact = {
            "name": "John Doe",
            "email": "john@example.com",
            "company": "Tech Corp"
        }
        is_valid, message = ContactValidator.validate_contact(contact)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid")
    
    def test_validate_contact_missing_email(self):
        """Test validation with missing required email field."""
        contact = {"name": "John Doe"}
        is_valid, message = ContactValidator.validate_contact(contact)
        self.assertFalse(is_valid)
        self.assertIn("Missing required fields", message)
    
    def test_validate_contact_invalid_email(self):
        """Test validation with invalid email format."""
        contact = {"email": "not-an-email"}
        is_valid, message = ContactValidator.validate_contact(contact)
        self.assertFalse(is_valid)
        self.assertIn("Invalid email", message)
    
    def test_validate_contact_custom_required_fields(self):
        """Test validation with custom required fields."""
        contact = {"email": "test@example.com"}
        is_valid, message = ContactValidator.validate_contact(
            contact, 
            required_fields=['email', 'name']
        )
        self.assertFalse(is_valid)
        self.assertIn("name", message)


if __name__ == '__main__':
    unittest.main()
