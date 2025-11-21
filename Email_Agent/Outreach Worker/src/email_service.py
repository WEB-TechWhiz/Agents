
"""Email service configurations for various providers."""

from typing import Dict


class EmailServiceConfig:
    """Predefined email service configurations."""
    
    SERVICES = {
        'gmail': {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Gmail SMTP (requires App Password)'
        },
        'outlook': {
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Outlook/Hotmail SMTP'
        },
        'yahoo': {
            'smtp_server': 'smtp.mail.yahoo.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Yahoo Mail SMTP'
        },
        'office365': {
            'smtp_server': 'smtp.office365.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Office 365 SMTP'
        },
        'sendgrid': {
            'smtp_server': 'smtp.sendgrid.net',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'SendGrid SMTP (API Key as password)'
        },
        'mailgun': {
            'smtp_server': 'smtp.mailgun.org',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Mailgun SMTP'
        },
        'zoho': {
            'smtp_server': 'smtp.zoho.com',
            'smtp_port': 587,
            'use_tls': True,
            'description': 'Zoho Mail SMTP'
        }
    }
    
    @classmethod
    def get_config(cls, service: str) -> Dict:
        """
        Get configuration for a specific email service.
        
        Args:
            service: Service name (e.g., 'gmail', 'outlook')
            
        Returns:
            Dictionary with SMTP configuration
            
        Raises:
            ValueError: If service is not found
        """
        service_lower = service.lower()
        if service_lower in cls.SERVICES:
            return cls.SERVICES[service_lower]
        raise ValueError(
            f"Unknown service: {service}. Available: {list(cls.SERVICES.keys())}"
        )
    
    @classmethod
    def list_services(cls) -> None:
        """Print available email services with descriptions."""
        print("Available Email Services:")
        print("-" * 60)
        for service, config in cls.SERVICES.items():
            print(f"{service.upper():12} - {config['description']}")
        print("-" * 60)
