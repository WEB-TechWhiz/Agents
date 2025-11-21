"""Test cases for email_service module."""

import unittest
from src.email_service import EmailServiceConfig


class TestEmailServiceConfig(unittest.TestCase):
    """Test cases for EmailServiceConfig class."""
    
    def test_get_config_gmail(self):
        """Test getting Gmail configuration."""
        config = EmailServiceConfig.get_config('gmail')
        self.assertEqual(config['smtp_server'], 'smtp.gmail.com')
        self.assertEqual(config['smtp_port'], 587)
        self.assertTrue(config['use_tls'])
    
    def test_get_config_outlook(self):
        """Test getting Outlook configuration."""
        config = EmailServiceConfig.get_config('outlook')
        self.assertEqual(config['smtp_server'], 'smtp-mail.outlook.com')
        self.assertEqual(config['smtp_port'], 587)
        self.assertTrue(config['use_tls'])
    
    def test_get_config_yahoo(self):
        """Test getting Yahoo configuration."""
        config = EmailServiceConfig.get_config('yahoo')
        self.assertEqual(config['smtp_server'], 'smtp.mail.yahoo.com')
        self.assertEqual(config['smtp_port'], 587)
    
    def test_get_config_office365(self):
        """Test getting Office 365 configuration."""
        config = EmailServiceConfig.get_config('office365')
        self.assertEqual(config['smtp_server'], 'smtp.office365.com')
        self.assertEqual(config['smtp_port'], 587)
    
    def test_get_config_case_insensitive(self):
        """Test that service names are case-insensitive."""
        config_lower = EmailServiceConfig.get_config('gmail')
        config_upper = EmailServiceConfig.get_config('GMAIL')
        config_mixed = EmailServiceConfig.get_config('GmAiL')
        
        self.assertEqual(config_lower, config_upper)
        self.assertEqual(config_lower, config_mixed)
    
    def test_get_config_unknown_service(self):
        """Test error handling for unknown service."""
        with self.assertRaises(ValueError) as context:
            EmailServiceConfig.get_config('unknown_service')
        
        self.assertIn('Unknown service', str(context.exception))
    
    def test_all_services_have_required_fields(self):
        """Test that all services have required configuration fields."""
        required_fields = ['smtp_server', 'smtp_port', 'use_tls', 'description']
        
        for service_name in EmailServiceConfig.SERVICES.keys():
            config = EmailServiceConfig.get_config(service_name)
            for field in required_fields:
                with self.subTest(service=service_name, field=field):
                    self.assertIn(field, config)
    
    def test_list_services(self):
        """Test that list_services runs without error."""
        # This just ensures the method doesn't crash
        try:
            EmailServiceConfig.list_services()
        except Exception as e:
            self.fail(f"list_services() raised {type(e).__name__} unexpectedly!")


if __name__ == '__main__':
    unittest.main()
