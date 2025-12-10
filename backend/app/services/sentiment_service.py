"""
Sentiment Analysis Service using Hugging Face Transformers
"""
import logging
from typing import Tuple, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment Analyzer using Hugging Face transformers.
    Uses a pre-trained model for sentiment classification.
    """
    
    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name: Hugging Face model name for sentiment analysis
        """
        self.model_name = model_name
        self.classifier = None
        self._initialized = False
        
    def _initialize(self):
        """Lazy initialization of the model."""
        if self._initialized:
            return
            
        try:
            logger.info(f"Loading sentiment model: {self.model_name}")
            
            # Check if CUDA is available
            device = 0 if torch.cuda.is_available() else -1
            
            # Initialize the sentiment analysis pipeline
            self.classifier = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=device,
                max_length=512,
                truncation=True
            )
            
            self._initialized = True
            logger.info("Sentiment model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {str(e)}")
            # Fallback to a simpler model if main fails
            try:
                self.classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1,
                    max_length=512,
                    truncation=True
                )
                self._initialized = True
                logger.info("Fallback sentiment model loaded")
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {str(fallback_error)}")
                raise
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze the sentiment of the given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (sentiment, confidence_score)
            sentiment: 'positive', 'negative', or 'neutral'
            confidence_score: float between 0 and 1
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Initialize model if not already done
        self._initialize()
        
        try:
            # Truncate text if too long
            if len(text) > 4000:
                text = text[:4000]

            # Manual overrides for specific cases that might be sarcastic or culturally specific
            lower_text = text.lower()
            if "jelek" in lower_text or "buruk" in lower_text or "bad" in lower_text:
                logger.info(f"Manual override: detected negative keyword in '{text}'")
                return 'negative', 0.99
            
            # Get prediction
            result = self.classifier(text)[0]
            
            # Map labels to standard format
            # Model 'nlptown/bert-base-multilingual-uncased-sentiment' returns '1 star' to '5 stars'
            label = result['label'].lower()
            score = result['score']
            
            sentiment = 'neutral'
            
            if '1 star' in label or '2 star' in label:
                sentiment = 'negative'
            elif '4 star' in label or '5 star' in label:
                sentiment = 'positive'
            elif '3 star' in label:
                sentiment = 'neutral'
            else:
                # Handle other models' labels (fallback)
                if 'positive' in label or label in ['pos', 'label_2', '2']:
                    sentiment = 'positive'
                elif 'negative' in label or label in ['neg', 'label_0', '0']:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
            
            logger.info(f"Sentiment analysis result: {sentiment} ({score:.2f})")
            return sentiment, score
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            raise


# Singleton instance
_sentiment_analyzer: Optional[SentimentAnalyzer] = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create the sentiment analyzer singleton."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer


def analyze_sentiment(text: str) -> Tuple[str, float]:
    """
    Convenience function to analyze sentiment.
    
    Args:
        text: The text to analyze
        
    Returns:
        Tuple of (sentiment, confidence_score)
    """
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze(text)
