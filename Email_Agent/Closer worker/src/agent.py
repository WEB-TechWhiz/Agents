import os
from .models import Lead, Proposal, LeadStatus, ProposalOption
from .generators import ProposalGenerator, PDFGenerator, SchedulingHelper

class CloserAgent:
    def __init__(self, template_dir: str = "src/templates", escalation_threshold: float = 10000.0):
        self.proposal_gen = ProposalGenerator(template_dir)
        self.pdf_gen = PDFGenerator()
        self.scheduler = SchedulingHelper()
        self.escalation_threshold = escalation_threshold
        
    def process_lead(self, lead: Lead, product_name: str = "Premium Service"):
        print(f"Processing lead: {lead.email} (ACV: ${lead.acv})")
        
        # 1. Check Escalation
        if self.check_escalation(lead):
            print(f"ESCALATING: Lead {lead.email} has high ACV (${lead.acv}). Handing over to human.")
            lead.status = LeadStatus.ESCALATED
            return {
                "status": "escalated",
                "reason": "High ACV"
            }
            
        # 2. Generate Proposal
        proposal = self._create_proposal_object(lead, product_name)
        
        # 3. Generate Content
        booking_link = self.scheduler.get_booking_link(lead.email)
        email_body = self.proposal_gen.generate_email_body(proposal, booking_link)
        quote_text = self.proposal_gen.generate_quote_text(proposal)
        
        # 4. Generate PDF
        pdf_filename = f"quote_{lead.email.split('@')[0]}.pdf"
        self.pdf_gen.create_quote_pdf(quote_text, pdf_filename)
        
        lead.status = LeadStatus.NEGOTIATING
        
        return {
            "status": "proposal_generated",
            "email_body": email_body,
            "pdf_path": pdf_filename
        }
        
    def check_escalation(self, lead: Lead) -> bool:
        return lead.acv > self.escalation_threshold

    def _create_proposal_object(self, lead: Lead, product_name: str) -> Proposal:
        # Logic to determine price/options based on lead info (Mock)
        return Proposal(
            lead=lead,
            product_name=product_name,
            price_range="$5,000 - $8,000",
            roi_estimate="300% in 6 months",
            timeline="4 weeks",
            options=[
                ProposalOption(name="Discovery Call", description="15-min chat", action_link=self.scheduler.get_booking_link(lead.email)),
                ProposalOption(name="Start Trial", description="14-day free access", action_link="https://app.example.com/signup"),
                ProposalOption(name="Send PO", description="Commit immediately")
            ]
        )
