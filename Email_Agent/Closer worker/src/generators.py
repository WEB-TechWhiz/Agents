import os
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
from datetime import datetime, timedelta
from .models import Proposal

class ProposalGenerator:
    def __init__(self, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def generate_email_body(self, proposal: Proposal, scheduling_link: str) -> str:
        template = self.env.get_template('closing_email.j2')
        return template.render(
            lead=proposal.lead,
            proposal=proposal,
            scheduling_link=scheduling_link
        )

    def generate_quote_text(self, proposal: Proposal) -> str:
        template = self.env.get_template('quote.txt')
        valid_until = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        return template.render(
            lead=proposal.lead,
            proposal=proposal,
            date=datetime.now().strftime("%Y-%m-%d"),
            valid_until=valid_until
        )

class PDFGenerator:
    def create_quote_pdf(self, text_content: str, output_path: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split text by lines and write
        for line in text_content.split('\n'):
            pdf.cell(200, 10, txt=line, ln=1, align='L')
            
        pdf.output(output_path)
        return output_path

class SchedulingHelper:
    def get_booking_link(self, lead_email: str) -> str:
        # Mock Calendly link
        return f"https://calendly.com/sales-team/meeting?email={lead_email}"
