
import sys
import os
sys.path.append(os.getcwd())

from app.services.sentiment_service import SentimentAnalyzer

def test_sentiment():
    analyzer = SentimentAnalyzer()
    
    test_cases = [
        "This product is okay, not great but not bad.",
        "Biasa aja sih, standar.", # Indonesian for "Just okay, standard."
        "Average quality.",
        "Lumayan lah.", # Indonesian for "Not bad / decent."
        "I have mixed feelings about this.",
        "Jelek banget", # Should be negative
        "Sangat bagus", # Should be positive
        "Not bad" # Specific edge case for manual override
    ]
    
    print("Testing Sentiment Analysis...")
    for text in test_cases:
        try:
            sentiment, score = analyzer.analyze(text)
            print(f"Text: '{text}' -> Sentiment: {sentiment} (Score: {score:.4f})")
        except Exception as e:
            print(f"Error analyzing '{text}': {e}")

if __name__ == "__main__":
    test_sentiment()
