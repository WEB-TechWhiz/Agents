import pytest
from src.classifiers import RuleBasedClassifier, LLMClassifier
from src.models import IntentType

def test_rule_based_unsubscribe():
    classifier = RuleBasedClassifier()
    text = "Please unsubscribe me immediately."
    result = classifier.classify(text)
    assert result is not None
    assert result.intent == IntentType.UNSUBSCRIBE

def test_rule_based_spam():
    classifier = RuleBasedClassifier()
    text = "You are a winner! Click here to claim your prize."
    result = classifier.classify(text)
    assert result is not None
    assert result.intent == IntentType.SPAM

def test_rule_based_no_match():
    classifier = RuleBasedClassifier()
    text = "I would like to know more about your services."
    result = classifier.classify(text)
    assert result is None

def test_llm_classifier_mock_interested():
    classifier = LLMClassifier()
    text = "I am interested in the price."
    result = classifier.classify(text)
    assert result.intent == IntentType.INTERESTED

def test_llm_classifier_mock_schedule():
    classifier = LLMClassifier()
    text = "Can we meet next week?"
    result = classifier.classify(text)
    assert result.intent == IntentType.SCHEDULE_REQUEST
