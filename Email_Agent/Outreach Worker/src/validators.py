"""Email validation and data validation utilities."""

import re
from typing import Dict, List, Tuple


class EmailValidator:
    """Email address validation utilities."""
    
    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(cls.EMAIL_PATTERN, email.strip()))
    
    @classmethod
    def validate_contacts(cls, contacts: List[Dict[str, str]]) -> Tuple[List[Dict], List[Dict]]:
        """
        Validate a list of contacts and separate valid from invalid.
        
        Args:
            contacts: List of contact dictionaries
            
        Returns:
            Tuple of (valid_contacts, invalid_contacts)
        """
        valid = []
        invalid = []
        
        for contact in contacts:
            email = contact.get('email', '')
            if cls.validate_email(email):
                valid.append(contact)
            else:
                invalid.append({
                    **contact,
                    'validation_error': 'Invalid email format'
                })
        
        return valid, invalid
    
    @classmethod
    def clean_email(cls, email: str) -> str:
        """
        Clean and normalize email address.
        
        Args:
            email: Email address to clean
            
        Returns:
            Cleaned email address
        """
        if not email:
            return ''
        return email.strip().lower()


class ContactValidator:
    """Contact data validation utilities."""
    
    REQUIRED_FIELDS = ['email']
    
    @classmethod
    def validate_contact(cls, contact: Dict[str, str], 
                        required_fields: List[str] = None) -> Tuple[bool, str]:
        """
        Validate a single contact dictionary.
        
        Args:
            contact: Contact dictionary
            required_fields: List of required field names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if required_fields is None:
            required_fields = cls.REQUIRED_FIELDS
        
        # Check required fields
        missing_fields = [field for field in required_fields if field not in contact]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate email
        if not EmailValidator.validate_email(contact.get('email', '')):
            return False, "Invalid email address"
        
        return True, "Valid"
