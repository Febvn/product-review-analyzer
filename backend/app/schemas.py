"""
Pydantic Schemas for Request/Response Validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Schema for creating a new review."""
    review_text: str = Field(..., min_length=10, max_length=5000, description="The review text to analyze")
    product_name: Optional[str] = Field(None, max_length=255, description="Optional product name")

    class Config:
        json_schema_extra = {
            "example": {
                "review_text": "This product is amazing! Great quality and fast shipping.",
                "product_name": "Wireless Headphones"
            }
        }


class SentimentResult(BaseModel):
    """Schema for sentiment analysis result."""
    sentiment: str = Field(..., description="Sentiment: positive, negative, or neutral")
    score: float = Field(..., ge=0, le=1, description="Confidence score between 0 and 1")


class KeyPointsResult(BaseModel):
    """Schema for key points extraction result."""
    key_points: List[str] = Field(..., description="List of extracted key points")


class ReviewResponse(BaseModel):
    """Schema for review response."""
    id: int
    review_text: str
    product_name: Optional[str] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    key_points: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    analysis_status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    success: bool
    message: str
    data: Optional[ReviewResponse] = None


class ReviewListResponse(BaseModel):
    """Schema for list of reviews response."""
    success: bool
    total: int
    reviews: List[ReviewResponse]


class ErrorResponse(BaseModel):
    """Schema for error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
