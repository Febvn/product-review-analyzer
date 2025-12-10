"""
API Routes for Review Analysis
"""
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Review
from app.schemas import (
    ReviewCreate, 
    ReviewResponse, 
    AnalysisResponse, 
    ReviewListResponse,
    ErrorResponse
)
from app.services import analyze_sentiment, extract_key_points

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["reviews"])


@router.post(
    "/analyze-review",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Review analyzed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def analyze_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """
    Analyze a new product review.
    
    - Performs sentiment analysis using Hugging Face
    - Extracts key points using Google Gemini
    - Saves results to PostgreSQL database
    
    Args:
        review_data: The review data to analyze
        db: Database session
        
    Returns:
        AnalysisResponse with the review analysis results
    """
    logger.info(f"Analyzing review: {review_data.review_text[:50]}...")
    
    # Create new review record
    review = Review(
        review_text=review_data.review_text,
        product_name=review_data.product_name,
        analysis_status="processing"
    )
    
    try:
        # Add to database (to get ID)
        db.add(review)
        db.commit()
        db.refresh(review)
        
        # Perform sentiment analysis
        try:
            sentiment, sentiment_score = analyze_sentiment(review_data.review_text)
            review.sentiment = sentiment
            review.sentiment_score = sentiment_score
            logger.info(f"Sentiment: {sentiment} ({sentiment_score:.2f})")
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            review.error_message = f"Sentiment analysis failed: {str(e)}"
        
        # Extract key points
        try:
            key_points = extract_key_points(
                review_data.review_text, 
                review_data.product_name
            )
            review.key_points = key_points
            logger.info(f"Extracted {len(key_points)} key points")
        except Exception as e:
            logger.error(f"Key points extraction failed: {str(e)}")
            if review.error_message:
                review.error_message += f"; Key points extraction failed: {str(e)}"
            else:
                review.error_message = f"Key points extraction failed: {str(e)}"
        
        # Update status
        if review.sentiment and review.key_points:
            review.analysis_status = "completed"
        elif review.sentiment or review.key_points:
            review.analysis_status = "partial"
        else:
            review.analysis_status = "failed"
        
        # Save to database
        db.commit()
        db.refresh(review)
        
        return AnalysisResponse(
            success=True,
            message="Review analyzed successfully" if review.analysis_status == "completed" 
                    else "Review analysis partially completed",
            data=ReviewResponse.model_validate(review)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing review: {str(e)}")
        db.rollback()
        
        # Update review status to failed
        try:
            review.analysis_status = "failed"
            review.error_message = str(e)
            db.commit()
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze review: {str(e)}"
        )


@router.get(
    "/reviews",
    response_model=ReviewListResponse,
    responses={
        200: {"description": "Reviews retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_reviews(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    db: Session = Depends(get_db)
) -> ReviewListResponse:
    """
    Get all reviews with pagination and optional filtering.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        sentiment: Optional filter by sentiment (positive, negative, neutral)
        db: Database session
        
    Returns:
        ReviewListResponse with list of reviews
    """
    logger.info(f"Fetching reviews (skip={skip}, limit={limit}, sentiment={sentiment})")
    
    try:
        # Build query
        query = db.query(Review)
        
        # Apply sentiment filter if provided
        if sentiment:
            sentiment_lower = sentiment.lower()
            if sentiment_lower not in ['positive', 'negative', 'neutral']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid sentiment filter. Must be: positive, negative, or neutral"
                )
            query = query.filter(Review.sentiment == sentiment_lower)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        reviews = query.order_by(desc(Review.created_at)).offset(skip).limit(limit).all()
        
        return ReviewListResponse(
            success=True,
            total=total,
            reviews=[ReviewResponse.model_validate(r) for r in reviews]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch reviews: {str(e)}"
        )


@router.get(
    "/reviews/{review_id}",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Review retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Review not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_review(
    review_id: int,
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """
    Get a specific review by ID.
    
    Args:
        review_id: The ID of the review to retrieve
        db: Database session
        
    Returns:
        AnalysisResponse with the review data
    """
    logger.info(f"Fetching review {review_id}")
    
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            raise HTTPException(
                status_code=404,
                detail=f"Review with id {review_id} not found"
            )
        
        return AnalysisResponse(
            success=True,
            message="Review retrieved successfully",
            data=ReviewResponse.model_validate(review)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching review {review_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch review: {str(e)}"
        )


@router.delete(
    "/reviews/{review_id}",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Review deleted successfully"},
        404: {"model": ErrorResponse, "description": "Review not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """
    Delete a specific review by ID.
    
    Args:
        review_id: The ID of the review to delete
        db: Database session
        
    Returns:
        AnalysisResponse confirming deletion
    """
    logger.info(f"Deleting review {review_id}")
    
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            raise HTTPException(
                status_code=404,
                detail=f"Review with id {review_id} not found"
            )
        
        db.delete(review)
        db.commit()
        
        return AnalysisResponse(
            success=True,
            message=f"Review {review_id} deleted successfully",
            data=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting review {review_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete review: {str(e)}"
        )
