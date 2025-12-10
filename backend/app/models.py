"""
Database Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from app.database import Base


class Review(Base):
    """
    Review model for storing product reviews and their analysis results.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Review content
    review_text = Column(Text, nullable=False)
    product_name = Column(String(255), nullable=True)
    
    # Sentiment analysis results
    sentiment = Column(String(50), nullable=True)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # confidence score 0-1
    
    # Key points extracted by Gemini
    key_points = Column(JSON, nullable=True)  # List of key points
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analysis status
    analysis_status = Column(String(50), default="pending")  # pending, completed, failed
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Review(id={self.id}, sentiment={self.sentiment})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "review_text": self.review_text,
            "product_name": self.product_name,
            "sentiment": self.sentiment,
            "sentiment_score": self.sentiment_score,
            "key_points": self.key_points,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "analysis_status": self.analysis_status,
            "error_message": self.error_message
        }
