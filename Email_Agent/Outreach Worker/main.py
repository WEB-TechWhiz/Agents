import os
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.agent import OutreachAgent
from src.utils import load_contacts_from_csv, ensure_directory, generate_log_filename
from src.templates import HTMLTemplates

def main():
    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Outreach Worker - Email Campaign Automation")
    parser.add_argument("--contacts", default="data/contacts.csv", help="Path to contacts CSV file")
    parser.add_argument("--subject", default="Elevate Your Digital Presence with Expert Web Solutions", help="Email subject template")
    parser.add_argument("--body", default="Hi {name},\n\nI hope this email finds you well.", help="Email body template")
    parser.add_argument("--html", action="store_true", help="Send as HTML email")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sending without actual delivery")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between emails in seconds")
    
    args = parser.parse_args()
    
    # Validate configuration
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    service = os.getenv("EMAIL_SERVICE", "gmail")
    
    if not email or not password:
        print("Error: EMAIL_ADDRESS and EMAIL_PASSWORD must be set in .env file")
        sys.exit(1)
        
    # Validate contacts file
    contacts_path = Path(args.contacts)
    if not contacts_path.exists():
        print(f"Error: Contacts file not found at {contacts_path}")
        print("Please create a contacts CSV file with 'email' and 'name' columns.")
        sys.exit(1)
        
    # Load contacts
    try:
        contacts = load_contacts_from_csv(str(contacts_path))
        if not contacts:
            print("Error: No contacts found in CSV file")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading contacts: {e}")
        sys.exit(1)
        
    print(f"Loaded {len(contacts)} contacts from {contacts_path}")
    
    if args.dry_run:
        print("\n--- DRY RUN MODE ---")
        print(f"Would send from: {email} via {service}")
        print(f"Subject template: {args.subject}")
        print(f"Body template: {args.body}")
        print("--- Contacts to process ---")
        for contact in contacts:
            print(f"- {contact.get('name', 'Unknown')} <{contact.get('email', 'No Email')}>")
        return

    # Initialize Agent
    try:
        agent = OutreachAgent(email, password, service)
        
        # Test connection first
        success, msg = agent.test_connection()
        if not success:
            print(f"Error connecting to email server: {msg}")
            sys.exit(1)
            
        print("Successfully connected to email server.")
        
        # Load professional HTML template
        template_path = "templates/html/professional.html"
        
        # Execute Campaign
        print("\nStarting campaign...")
        print(f"Using template: {template_path}\n")
        
        # Process each contact with the professional template
        results = {
            'sent': 0, 
            'failed': 0, 
            'skipped': 0,
            'failed_emails': [],
            'start_time': None,
            'end_time': None
        }
        
        from datetime import datetime
        import time
        results['start_time'] = datetime.now().isoformat()
        
        for i, contact in enumerate(contacts):
            email_addr = contact.get('email', '')
            name = contact.get('name', 'there')
            company = contact.get('company', 'your organization')
            
            print(f"\n[{i+1}/{len(contacts)}] Processing: {name} <{email_addr}>")
            
            # Load and personalize the HTML template
            try:
                html_body = HTMLTemplates.load_from_file(
                    template_path,
                    name=name,
                    company=company,
                    sender_email=email
                )
                
                # Personalize subject
                from string import Template
                subject_tmpl = Template(args.subject)
                subject = subject_tmpl.safe_substitute(contact)
                
                # Send email
                success, error_msg = agent.send_email_with_retry(
                    recipient=email_addr,
                    subject=subject,
                    body=html_body,
                    html=True
                )
                
                if success:
                    results['sent'] += 1
                    print(f"✓ Successfully sent to {email_addr}")
                else:
                    results['failed'] += 1
                    results['failed_emails'].append({'email': email_addr, 'error': error_msg})
                    print(f"✗ Failed to send to {email_addr}: {error_msg}")
                
                # Delay between emails
                if i < len(contacts) - 1:
                    time.sleep(args.delay)
                    
            except Exception as e:
                results['failed'] += 1
                results['failed_emails'].append({'email': email_addr, 'error': str(e)})
                print(f"✗ Error processing {email_addr}: {e}")
        
        results['end_time'] = datetime.now().isoformat()
        
        # Save logs and report
        log_dir = ensure_directory("logs")
        log_file = log_dir / generate_log_filename()
        agent.save_log(str(log_file))
        
        print(agent.generate_report(results))
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
