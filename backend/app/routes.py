"""
API Routes untuk Review Analysis
File ini mendefinisikan semua endpoint API untuk operasi CRUD review.
Setiap endpoint menangani satu operasi spesifik (create, read, update, delete).
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

# Setup logger untuk tracking
logger = logging.getLogger(__name__)

# ==========================================
# ROUTER SETUP
# ==========================================
"""
APIRouter adalah grouping untuk endpoints yang related.
Semua endpoint di file ini akan memiliki prefix '/api' dan tag 'reviews'.

Contoh:
- POST /api/analyze-review
- GET /api/reviews
- GET /api/reviews/{id}
- DELETE /api/reviews/{id}
"""
router = APIRouter(
    prefix="/api",      # Prefix untuk semua routes di router ini
    tags=["reviews"]    # Tag untuk grouping di Swagger UI
)


# ==========================================
# ENDPOINT 1: ANALYZE REVIEW
# ==========================================
@router.post(
    "/analyze-review",
    response_model=AnalysisResponse,  # Schema untuk response
    responses={
        200: {"description": "Review analyzed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def analyze_review(
    review_data: ReviewCreate,       # Request body (auto-validated by Pydantic)
    db: Session = Depends(get_db)    # Dependency injection: database session
) -> AnalysisResponse:
    """
    Endpoint untuk menganalisis review baru.
    
    Proses:
    1. Terima request body berisi review_text dan product_name
    2. Simpan review ke database dengan status 'processing'
    3. Jalankan analisis sentimen menggunakan Hugging Face
    4. Ekstrak key points menggunakan Gemini AI (atau fallback)
    5. Update status dan simpan hasil ke database
    6. Return hasil analisis
    
    Args:
        review_data: Data review dari request body
            - review_text (str): Teks review (10-5000 karakter)
            - product_name (str, optional): Nama produk
        db: Database session (auto-injected)
        
    Returns:
        AnalysisResponse berisi:
            - success (bool): True jika berhasil
            - message (str): Pesan status
            - data (ReviewResponse): Detail review dan hasil analisis
            
    Raises:
        HTTPException 500: Jika terjadi error saat proses analisis
        
    Contoh Request:
        POST /api/analyze-review
        {
            "review_text": "Produk bagus, pengiriman cepat!",
            "product_name": "Laptop ASUS"
        }
        
    Contoh Response:
        {
            "success": true,
            "message": "Review analyzed successfully",
            "data": {
                "id": 1,
                "review_text": "Produk bagus, pengiriman cepat!",
                "product_name": "Laptop ASUS",
                "sentiment": "positive",
                "sentiment_score": 0.95,
                "key_points": ["Kualitas produk bagus", "Pengiriman cepat"],
                "analysis_status": "completed"
            }
        }
    """
    logger.info(f"Analyzing review: {review_data.review_text[:50]}...")
    
    # Buat record review baru di database
    review = Review(
        review_text=review_data.review_text,
        product_name=review_data.product_name,
        analysis_status="processing"  # Status awal: processing
    )
    
    try:
        # ==========================================
        # STEP 1: Simpan ke database (untuk mendapatkan ID)
        # ==========================================
        db.add(review)              # Add review ke session
        db.commit()                 # Commit ke database (INSERT)
        db.refresh(review)          # Refresh untuk mendapat ID dan timestamp
        
        # ==========================================
        # STEP 2: Analisis Sentimen
        # ==========================================
        try:
            # Panggil service sentiment analysis
            sentiment, sentiment_score = analyze_sentiment(review_data.review_text)
            
            # Simpan hasil ke review object
            review.sentiment = sentiment
            review.sentiment_score = sentiment_score
            
            logger.info(f"Sentiment: {sentiment} ({sentiment_score:.2f})")
        except Exception as e:
            # Jika sentiment analysis gagal, log error tapi lanjutkan proses
            logger.error(f"Sentiment analysis failed: {str(e)}")
            review.error_message = f"Sentiment analysis failed: {str(e)}"
        
        # ==========================================
        # STEP 3: Ekstraksi Key Points
        # ==========================================
        try:
            # Panggil service key points extraction
            key_points = extract_key_points(
                review_data.review_text, 
                review_data.product_name  # Nama produk untuk konteks
            )
            
            # Simpan hasil ke review object
            review.key_points = key_points
            
            logger.info(f"Extracted {len(key_points)} key points")
        except Exception as e:
            # Jika ekstraksi gagal, log error tapi lanjutkan proses
            logger.error(f"Key points extraction failed: {str(e)}")
            
            # Append error message (jika sudah ada error sebelumnya)
            if review.error_message:
                review.error_message += f"; Key points extraction failed: {str(e)}"
            else:
                review.error_message = f"Key points extraction failed: {str(e)}"
        
        # ==========================================
        # STEP 4: Update Status Berdasarkan Hasil
        # ==========================================
        if review.sentiment and review.key_points:
            # Kedua analisis berhasil
            review.analysis_status = "completed"
        elif review.sentiment or review.key_points:
            # Salah satu berhasil
            review.analysis_status = "partial"
        else:
            # Kedua gagal
            review.analysis_status = "failed"
        
        # ==========================================
        # STEP 5: Commit hasil akhir ke database
        # ==========================================
        db.commit()        # UPDATE review dengan hasil analisis
        db.refresh(review) # Refresh untuk mendapat timestamp terbaru
        
        # ==========================================
        # STEP 6: Return response
        # ==========================================
        return AnalysisResponse(
            success=True,
            message="Review analyzed successfully" if review.analysis_status == "completed" 
                    else "Review analysis partially completed",
            data=ReviewResponse.model_validate(review)  # Convert SQLAlchemy -> Pydantic
        )
        
    except Exception as e:
        # ==========================================
        # ERROR HANDLING
        # ==========================================
        logger.error(f"Error analyzing review: {str(e)}")
        db.rollback()  # Rollback jika terjadi error
        
        # Coba update status ke failed
        try:
            review.analysis_status = "failed"
            review.error_message = str(e)
            db.commit()
        except:
            pass  # Ignore jika gagal update
        
        # Raise HTTPException (akan dikembalikan sebagai error response)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze review: {str(e)}"
        )


# ==========================================
# ENDPOINT 2: GET ALL REVIEWS (with Pagination & Filter)
# ==========================================
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
    Mendapatkan list reviews dengan pagination dan filter.
    
    Fitur:
    - Pagination: skip dan limit untuk lazy loading
    - Filter: filter berdasarkan sentiment
    - Sorting: Otomatis diurutkan dari yang terbaru
    
    Args:
        skip (int): Jumlah record yang di-skip (untuk pagination)
            - Default: 0
            - Range: >= 0
            - Contoh: skip=10 artinya skip 10 record pertama
            
        limit (int): Maksimal jumlah record yang dikembalikan
            - Default: 50
            - Range: 1-100
            - Contoh: limit=20 artinya ambil maksimal 20 records
            
        sentiment (str, optional): Filter berdasarkan sentiment
            - Valid values: "positive", "negative", "neutral"
            - Jika None, return semua sentiment
            
        db: Database session (auto-injected)
        
    Returns:
        ReviewListResponse berisi:
            - success (bool): True jika berhasil
            - total (int): Total jumlah reviews (untuk pagination)
            - reviews (List[ReviewResponse]): List reviews
            
    Raises:
        HTTPException 400: Jika sentiment filter invalid
        HTTPException 500: Jika terjadi error database
        
    Contoh Request 1 (Basic):
        GET /api/reviews
        
    Contoh Request 2 (Pagination):
        GET /api/reviews?skip=10&limit=20
        (Ambil 20 reviews mulai dari index 10)
        
    Contoh Request 3 (Filter + Pagination):
        GET /api/reviews?sentiment=positive&skip=0&limit=10
        (Ambil 10 reviews positive pertama)
        
    Contoh Response:
        {
            "success": true,
            "total": 100,
            "reviews": [
                { "id": 1, "review_text": "...", "sentiment": "positive", ... },
                { "id": 2, "review_text": "...", "sentiment": "negative", ... },
                ...
            ]
        }
    """
    logger.info(f"Fetching reviews (skip={skip}, limit={limit}, sentiment={sentiment})")
    
    try:
        # ==========================================
        # BUILD QUERY
        # ==========================================
        # Mulai dengan base query
        query = db.query(Review)
        
        # ==========================================
        # APPLY FILTER (jika ada)
        # ==========================================
        if sentiment:
            # Validasi sentiment value
            sentiment_lower = sentiment.lower()
            if sentiment_lower not in ['positive', 'negative', 'neutral']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid sentiment filter. Must be: positive, negative, or neutral"
                )
            
            # Apply filter
            query = query.filter(Review.sentiment == sentiment_lower)
        
        # ==========================================
        # COUNT TOTAL (untuk pagination info)
        # ==========================================
        total = query.count()
        
        # ==========================================
        # APPLY PAGINATION & SORTING
        # ==========================================
        reviews = query.order_by(
            desc(Review.created_at)  # Urutkan dari yang terbaru
        ).offset(skip).limit(limit).all()
        
        # ==========================================
        # RETURN RESPONSE
        # ==========================================
        return ReviewListResponse(
            success=True,
            total=total,
            reviews=[ReviewResponse.model_validate(r) for r in reviews]
        )
        
    except HTTPException:
        # Re-raise HTTPException (sudah di-handle)
        raise
    except Exception as e:
        # Catch semua error lainnya
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch reviews: {str(e)}"
        )


# ==========================================
# ENDPOINT 3: GET REVIEW BY ID
# ==========================================
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
    review_id: int,                   # Path parameter
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """
    Mendapatkan detail review berdasarkan ID.
    
    Args:
        review_id (int): ID review yang ingin diambil
        db: Database session (auto-injected)
        
    Returns:
        AnalysisResponse berisi detail review
        
    Raises:
        HTTPException 404: Jika review dengan ID tersebut tidak ditemukan
        HTTPException 500: Jika terjadi error database
        
    Contoh Request:
        GET /api/reviews/1
        
    Contoh Response (Success):
        {
            "success": true,
            "message": "Review retrieved successfully",
            "data": {
                "id": 1,
                "review_text": "Produk bagus!",
                "sentiment": "positive",
                ...
            }
        }
        
    Contoh Response (Not Found):
        {
            "detail": "Review with id 999 not found"
        }
    """
    logger.info(f"Fetching review {review_id}")
    
    try:
        # ==========================================
        # QUERY DATABASE
        # ==========================================
        review = db.query(Review).filter(Review.id == review_id).first()
        
        # ==========================================
        # CHECK IF EXISTS
        # ==========================================
        if not review:
            raise HTTPException(
                status_code=404,
                detail=f"Review with id {review_id} not found"
            )
        
        # ==========================================
        # RETURN RESPONSE
        # ==========================================
        return AnalysisResponse(
            success=True,
            message="Review retrieved successfully",
            data=ReviewResponse.model_validate(review)
        )
        
    except HTTPException:
        # Re-raise HTTPException
        raise
    except Exception as e:
        logger.error(f"Error fetching review {review_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch review: {str(e)}"
        )


# ==========================================
# ENDPOINT 4: DELETE REVIEW
# ==========================================
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
    review_id: int,                   # Path parameter
    db: Session = Depends(get_db)
) -> AnalysisResponse:
    """
    Menghapus review berdasarkan ID.
    
    PERHATIAN: Operasi ini PERMANEN dan tidak bisa di-undo!
    
    Args:
        review_id (int): ID review yang ingin dihapus
        db: Database session (auto-injected)
        
    Returns:
        AnalysisResponse dengan data=None (konfirmasi delete)
        
    Raises:
        HTTPException 404: Jika review dengan ID tersebut tidak ditemukan
        HTTPException 500: Jika terjadi error saat delete
        
    Contoh Request:
        DELETE /api/reviews/1
        
    Contoh Response (Success):
        {
            "success": true,
            "message": "Review 1 deleted successfully",
            "data": null
        }
        
    Contoh Response (Not Found):
        {
            "detail": "Review with id 999 not found"
        }
    """
    logger.info(f"Deleting review {review_id}")
    
    try:
        # ==========================================
        # QUERY DATABASE
        # ==========================================
        review = db.query(Review).filter(Review.id == review_id).first()
        
        # ==========================================
        # CHECK IF EXISTS
        # ==========================================
        if not review:
            raise HTTPException(
                status_code=404,
                detail=f"Review with id {review_id} not found"
            )
        
        # ==========================================
        # DELETE FROM DATABASE
        # ==========================================
        db.delete(review)  # Mark untuk delete
        db.commit()        # Execute DELETE query
        
        # ==========================================
        # RETURN CONFIRMATION
        # ==========================================
        return AnalysisResponse(
            success=True,
            message=f"Review {review_id} deleted successfully",
            data=None  # Tidak ada data karena sudah dihapus
        )
        
    except HTTPException:
        # Re-raise HTTPException
        raise
    except Exception as e:
        logger.error(f"Error deleting review {review_id}: {str(e)}")
        db.rollback()  # Rollback jika error
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete review: {str(e)}"
        )
