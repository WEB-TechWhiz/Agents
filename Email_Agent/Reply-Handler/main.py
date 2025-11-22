import os
from dotenv import load_dotenv
from src.agent import IntentParserAgent

# Load environment variables
load_dotenv()

def main():
    # Initialize Agent
    api_key = os.getenv("OPENAI_API_KEY")
    agent = IntentParserAgent(llm_api_key=api_key)
    
    print("--- Reply-Handler Agent Started ---")
    
    # Sample 1: Unsubscribe
    email1 = """
    Hi,
    Please remove me from your list.
    Thanks.
    """
    print(f"\nProcessing Email 1:\n{email1}")
    result1 = agent.process_inbound(email1, "user1@example.com")
    print(f"Result: {result1.intent} (Confidence: {result1.confidence})")
    
    # Sample 2: Interested
    email2 = """
    Hello,
    I'm interested in your product. Can we schedule a call?
    Best,
    John
    """
    print(f"\nProcessing Email 2:\n{email2}")
    result2 = agent.process_inbound(email2, "user2@example.com")
    print(f"Result: {result2.intent} (Confidence: {result2.confidence})")
    if result2.meeting_time:
        print(f"Meeting Time: {result2.meeting_time}")

if __name__ == "__main__":
    main()
