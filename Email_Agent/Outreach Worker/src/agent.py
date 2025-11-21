"""Main OutreachAgent class."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from string import Template
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import time
from datetime import datetime

from .email_service import EmailServiceConfig
from .templates import HTMLTemplates
from .validators import EmailValidator, ContactValidator


class OutreachAgent:
    """
    Enhanced outreach agent with retry logic, HTML templates, 
    and multiple email service support.
    """
    
    def __init__(self, email: str, password: str, service: str = 'gmail', 
                 custom_smtp: Optional[Dict] = None):
        """
        Initialize the outreach agent.
        
        Args:
            email: Sender email address
            password: Email password or app-specific password
            service: Email service name ('gmail', 'outlook', 'yahoo', etc.)
            custom_smtp: Custom SMTP configuration
        """
        self.sender_email = email
        self.password = password
        
        if custom_smtp:
            self.smtp_server = custom_smtp['smtp_server']
            self.smtp_port = custom_smtp['smtp_port']
            self.use_tls = custom_smtp.get('use_tls', True)
        else:
            config = EmailServiceConfig.get_config(service)
            self.smtp_server = config['smtp_server']
            self.smtp_port = config['smtp_port']
            self.use_tls = config['use_tls']
        
        self.sent_log = []
        self.retry_count = 3
        self.retry_delay = 5
        
    def generate_personalized_message(self, template: str, 
                                     contact: Dict[str, str]) -> str:
        """Generate personalized message from template."""
        template_obj = Template(template)
        try:
            return template_obj.safe_substitute(contact)
        except Exception as e:
            print(f"Error generating message: {e}")
            return template
    
    def attach_document(self, msg: MIMEMultipart, file_path: str) -> bool:
        """Attach document to email message."""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = Path(file_path).name
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)
            return True
        except Exception as e:
            print(f"Error attaching document {file_path}: {e}")
            return False
    
    def send_email_with_retry(self, 
                              recipient: str, 
                              subject: str, 
                              body: str, 
                              attachments: Optional[List[str]] = None,
                              html: bool = False,
                              max_retries: Optional[int] = None) -> Tuple[bool, str]:
        """Send email with automatic retry logic."""
        if not EmailValidator.validate_email(recipient):
            return False, f"Invalid email address: {recipient}"
        
        max_retries = max_retries if max_retries is not None else self.retry_count
        last_error = ""
        
        for attempt in range(max_retries):
            try:
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                
                mime_type = 'html' if html else 'plain'
                msg.attach(MIMEText(body, mime_type))
                
                if attachments:
                    for file_path in attachments:
                        if not self.attach_document(msg, file_path):
                            print(f"Warning: Failed to attach {file_path}")
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.password)
                    server.send_message(msg)
                
                self.sent_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'recipient': recipient,
                    'subject': subject,
                    'status': 'sent',
                    'attempt': attempt + 1
                })
                return True, "Success"
                
            except smtplib.SMTPAuthenticationError as e:
                last_error = f"Authentication failed: {str(e)}"
                print(f"Authentication error - no retry: {last_error}")
                break
                
            except (smtplib.SMTPException, ConnectionError, TimeoutError) as e:
                last_error = f"SMTP error: {str(e)}"
                print(f"Attempt {attempt + 1}/{max_retries} failed: {last_error}")
                
                if attempt < max_retries - 1:
                    wait_time = self.retry_delay * (attempt + 1)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                print(f"Attempt {attempt + 1}/{max_retries} failed: {last_error}")
                
                if attempt < max_retries - 1:
                    time.sleep(self.retry_delay)
        
        self.sent_log.append({
            'timestamp': datetime.now().isoformat(),
            'recipient': recipient,
            'subject': subject,
            'status': 'failed',
            'error': last_error,
            'attempts': max_retries
        })
        return False, last_error
    
    def send_bulk_outreach(self,
                          contacts: List[Dict[str, str]],
                          subject_template: str,
                          body_template: str,
                          attachments: Optional[List[str]] = None,
                          delay: float = 1.0,
                          html: bool = False,
                          html_template_type: str = 'professional',
                          html_title: str = "",
                          html_footer: str = "",
                          max_emails: Optional[int] = None,
                          skip_invalid: bool = True) -> Dict:
        """Send personalized emails to multiple contacts."""
        results = {
            'sent': 0, 
            'failed': 0, 
            'skipped': 0,
            'failed_emails': [],
            'start_time': datetime.now().isoformat()
        }
        
        contacts_to_process = contacts[:max_emails] if max_emails else contacts
        
        for i, contact in enumerate(contacts_to_process):
            email = contact.get('email', '')
            print(f"\n[{i+1}/{len(contacts_to_process)}] Processing: {email}")
            
            if not EmailValidator.validate_email(email):
                print(f"⚠ Invalid email address: {email}")
                if skip_invalid:
                    results['skipped'] += 1
                    continue
            
            subject = self.generate_personalized_message(subject_template, contact)
            body_content = self.generate_personalized_message(body_template, contact)
            
            if html:
                title = self.generate_personalized_message(html_title, contact) if html_title else ""
                footer = self.generate_personalized_message(html_footer, contact) if html_footer else ""
                
                if html_template_type == 'professional':
                    body = HTMLTemplates.professional_template(title, body_content, footer)
                elif html_template_type == 'simple':
                    body = HTMLTemplates.simple_template(body_content)
                else:
                    body = HTMLTemplates.minimal_template(body_content)
            else:
                body = body_content
            
            success, error_msg = self.send_email_with_retry(
                recipient=email,
                subject=subject,
                body=body,
                attachments=attachments,
                html=html
            )
            
            if success:
                results['sent'] += 1
                print(f"✓ Successfully sent to {email}")
            else:
                results['failed'] += 1
                results['failed_emails'].append({'email': email, 'error': error_msg})
                print(f"✗ Failed to send to {email}: {error_msg}")
            
            if i < len(contacts_to_process) - 1:
                time.sleep(delay)
        
        results['end_time'] = datetime.now().isoformat()
        return results
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test SMTP connection and authentication."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.password)
            return True, "Connection successful!"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def save_log(self, log_file: str):
        """Save sent email log to JSON file."""
        import json
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.sent_log, f, indent=2)
        print(f"\n📄 Log saved to {log_file}")
    
    def generate_report(self, results: Dict) -> str:
        """Generate formatted campaign report."""
        total_processed = results['sent'] + results['failed'] + results['skipped']
        success_rate = (results['sent'] / max(1, results['sent'] + results['failed']) * 100)
        
        report = f"""
{'='*70}
OUTREACH CAMPAIGN REPORT
{'='*70}
Start Time: {results.get('start_time', 'N/A')}
End Time: {results.get('end_time', 'N/A')}

SUMMARY:
--------
✓ Successfully Sent: {results['sent']}
✗ Failed: {results['failed']}
⚠ Skipped (Invalid): {results['skipped']}
Total Processed: {total_processed}

Success Rate: {success_rate:.1f}%
"""
        
        if results['failed_emails']:
            report += "\nFAILED EMAILS:\n--------------\n"
            for item in results['failed_emails']:
                report += f"• {item['email']}: {item['error']}\n"
        
        report += "=" * 70
        return report
