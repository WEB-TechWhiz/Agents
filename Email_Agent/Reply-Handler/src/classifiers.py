import re
from typing import Optional
from .models import IntentType, ExtractionResult

class RuleBasedClassifier:
    def classify(self, text: str) -> Optional[ExtractionResult]:
        text_lower = text.lower()
        
        # Unsubscribe patterns
        if re.search(r'\b(unsubscribe|stop|remove me)\b', text_lower):
            return ExtractionResult(
                intent=IntentType.UNSUBSCRIBE,
                confidence=1.0
            )
            
        # Spam patterns
        if re.search(r'\b(buy now|click here|winner|lottery)\b', text_lower):
             return ExtractionResult(
                intent=IntentType.SPAM,
                confidence=0.9
            )
            
        # Not Interested patterns
        if re.search(r'\b(not interested|no thanks|pass)\b', text_lower):
            return ExtractionResult(
                intent=IntentType.NOT_INTERESTED,
                confidence=0.9
            )
            
        return None

class LLMClassifier:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if not api_key:
            print("WARNING: No API key provided for LLMClassifier. Using mock mode.")
            self.llm = None
        else:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    openai_api_key=api_key,
                    temperature=0
                )
            except ImportError:
                print("ERROR: langchain_openai not installed. Using mock mode.")
                self.llm = None

    def classify(self, text: str) -> ExtractionResult:
        """
        Uses LLM to classify intent and extract data.
        """
        if not self.llm:
            # Fallback to mock if no LLM available
            return self._mock_classify(text)

        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import PydanticOutputParser

        parser = PydanticOutputParser(pydantic_object=ExtractionResult)

        prompt = PromptTemplate(
            template="""
            Analyze the following email and extract the intent and other structured data.
            
            Email Content:
            {text}
            
            {format_instructions}
            
            If the intent is ambiguous, choose the most likely one and lower the confidence.
            """,
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        try:
            result = chain.invoke({"text": text})
            return result
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._mock_classify(text)

    def _mock_classify(self, text: str) -> ExtractionResult:
        # Mock logic for demonstration purposes
        text_lower = text.lower()
        if "schedule" in text_lower or "meet" in text_lower:
            return ExtractionResult(
                intent=IntentType.SCHEDULE_REQUEST,
                confidence=0.85,
                meeting_time="Next Tuesday at 10am" # Mock extraction
            )
        elif "price" in text_lower or "cost" in text_lower or "interested" in text_lower:
             return ExtractionResult(
                intent=IntentType.INTERESTED,
                confidence=0.8,
                requested_product="General Inquiry"
            )
            
        return ExtractionResult(
            intent=IntentType.UNKNOWN,
            confidence=0.5
        )
