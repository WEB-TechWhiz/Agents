from .models import Lead, EmailLog, IntentType, ExtractionResult
from .classifiers import RuleBasedClassifier, LLMClassifier
from .utils import clean_text, detect_language
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentParserAgent:
    def __init__(self, llm_api_key: str = None):
        self.rule_classifier = RuleBasedClassifier()
        self.llm_classifier = LLMClassifier(api_key=llm_api_key)
        
    def process_inbound(self, email_content: str, sender_email: str) -> ExtractionResult:
        logger.info(f"Processing email from {sender_email}")
        
        # 1. Clean Text
        cleaned_text = clean_text(email_content)
        
        # 2. Detect Language
        language = detect_language(cleaned_text)
        
        # 3. Rule-Based Classification
        result = self.rule_classifier.classify(cleaned_text)
        if result:
            logger.info(f"Rule-based match: {result.intent}")
            result.language = language
            self._handle_actions(result, sender_email)
            return result
            
        # 4. LLM Classification (if no rule match)
        logger.info("No rule match, invoking LLM...")
        result = self.llm_classifier.classify(cleaned_text)
        result.language = language
        logger.info(f"LLM match: {result.intent}")
        
        self._handle_actions(result, sender_email)
        return result
    
    def _handle_actions(self, result: ExtractionResult, sender_email: str):
        # Update Lead State (Mock)
        logger.info(f"Updating lead {sender_email} state based on {result.intent}")
        
        # Trigger downstream agents
        if result.intent == IntentType.INTERESTED:
            self.trigger_closer_agent(sender_email, result)
        elif result.intent == IntentType.UNSUBSCRIBE:
            self.trigger_compliance_agent(sender_email, result)
            
    def trigger_closer_agent(self, email: str, result: ExtractionResult):
        logger.info(f"TRIGGER: Closer Agent for {email} (Product: {result.requested_product})")
        
    def trigger_compliance_agent(self, email: str, result: ExtractionResult):
        logger.info(f"TRIGGER: Compliance Agent for {email} (Unsubscribe)")
