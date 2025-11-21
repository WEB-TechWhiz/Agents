"""Test cases for agent module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.agent import OutreachAgent


class TestOutreachAgent(unittest.TestCase):
    """Test cases for OutreachAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = OutreachAgent(
            email="test@example.com",
            password="test_password",
            service="gmail"
        )
    
    def test_initialization_with_service(self):
        """Test agent initialization with predefined service."""
        agent = OutreachAgent("test@example.com", "password", "gmail")
        self.assertEqual(agent.sender_email, "test@example.com")
        self.assertEqual(agent.smtp_server, "smtp.gmail.com")
        self.assertEqual(agent.smtp_port, 587)
        self.assertTrue(agent.use_tls)
    
    def test_initialization_with_custom_smtp(self):
        """Test agent initialization with custom SMTP config."""
        custom_config = {
            'smtp_server': 'custom.smtp.com',
            'smtp_port': 465,
            'use_tls': False
        }
        agent = OutreachAgent(
            "test@example.com",
            "password",
            custom_smtp=custom_config
        )
        self.assertEqual(agent.smtp_server, "custom.smtp.com")
        self.assertEqual(agent.smtp_port, 465)
        self.assertFalse(agent.use_tls)
    
    def test_generate_personalized_message(self):
        """Test message personalization with template."""
        template = "Hello $name, welcome to $company!"
        contact = {"name": "John", "company": "Tech Corp"}
        
        result = self.agent.generate_personalized_message(template, contact)
        self.assertEqual(result, "Hello John, welcome to Tech Corp!")
    
    def test_generate_personalized_message_missing_fields(self):
        """Test message personalization with missing fields."""
        template = "Hello $name, welcome to $company!"
        contact = {"name": "John"}
        
        result = self.agent.generate_personalized_message(template, contact)
        # safe_substitute leaves missing variables as-is
        self.assertIn("John", result)
        self.assertIn("$company", result)
    
    @patch('src.agent.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        success, message = self.agent.send_email_with_retry(
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "Success")
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()
    
    def test_send_email_invalid_recipient(self):
        """Test sending email to invalid address."""
        success, message = self.agent.send_email_with_retry(
            recipient="invalid-email",
            subject="Test",
            body="Test"
        )
        
        self.assertFalse(success)
        self.assertIn("Invalid email", message)
    
    @patch('src.agent.smtplib.SMTP')
    def test_send_email_with_retry_on_failure(self, mock_smtp):
        """Test retry logic on temporary failure."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Simulate failure then success
        mock_server.send_message.side_effect = [
            ConnectionError("Temporary failure"),
            None  # Success on second attempt
        ]
        
        with patch('time.sleep'):  # Skip actual sleep delays
            success, message = self.agent.send_email_with_retry(
                recipient="test@example.com",
                subject="Test",
                body="Test",
                max_retries=2
            )
        
        self.assertTrue(success)
        self.assertEqual(mock_server.send_message.call_count, 2)
    
    @patch('src.agent.smtplib.SMTP')
    def test_test_connection_success(self, mock_smtp):
        """Test successful connection test."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        success, message = self.agent.test_connection()
        
        self.assertTrue(success)
        self.assertEqual(message, "Connection successful!")
        mock_server.login.assert_called_once()
    
    @patch('src.agent.smtplib.SMTP')
    def test_test_connection_failure(self, mock_smtp):
        """Test connection test failure."""
        mock_smtp.return_value.__enter__.side_effect = Exception("Connection failed")
        
        success, message = self.agent.test_connection()
        
        self.assertFalse(success)
        self.assertIn("Connection failed", message)
    
    def test_generate_report(self):
        """Test campaign report generation."""
        results = {
            'sent': 5,
            'failed': 2,
            'skipped': 1,
            'failed_emails': [
                {'email': 'fail1@test.com', 'error': 'Error 1'},
                {'email': 'fail2@test.com', 'error': 'Error 2'}
            ],
            'start_time': '2025-01-01T10:00:00',
            'end_time': '2025-01-01T10:05:00'
        }
        
        report = self.agent.generate_report(results)
        
        self.assertIn('5', report)  # sent count
        self.assertIn('2', report)  # failed count
        self.assertIn('fail1@test.com', report)
        self.assertIn('fail2@test.com', report)
    
    @patch('builtins.open', create=True)
    @patch('json.dump')
    @patch('builtins.print')  # Suppress print to avoid Unicode encoding issues
    def test_save_log(self, mock_print, mock_json_dump, mock_open):
        """Test log saving functionality."""
        self.agent.sent_log = [{'test': 'data'}]
        
        self.agent.save_log('test_log.json')
        
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()


if __name__ == '__main__':
    unittest.main()
