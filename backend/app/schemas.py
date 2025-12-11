"""
Pydantic Schemas untuk Validasi Request/Response
File ini mendefinisikan struktur data untuk API request dan response.
Pydantic melakukan validasi otomatis saat data masuk/keluar dari API.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """
    Schema untuk membuat review baru (Request Body).
    Digunakan saat user submit review untuk dianalisis.
    
    Validasi:
    - review_text: Minimal 10 karakter, maksimal 5000 karakter
    - product_name: Opsional, maksimal 255 karakter
    """
    review_text: str = Field(
        ...,  # ... artinya field wajib diisi (required)
        min_length=10,     # Minimal 10 karakter
        max_length=5000,   # Maksimal 5000 karakter
        description="The review text to analyze"
    )
    """
    Teks review yang akan dianalisis.
    
    Contoh valid:
        "Produk ini sangat bagus, pengiriman cepat!"
        
    Contoh invalid:
        "Bagus" (terlalu pendek, kurang dari 10 karakter)
    """
    
    product_name: Optional[str] = Field(
        None,  # None artinya opsional (tidak wajib)
        max_length=255,  # Maksimal 255 karakter
        description="Optional product name"
    )
    """
    Nama produk (opsional).
    Jika diisi, akan digunakan untuk memberikan konteks ke AI.
    """

    class Config:
        """
        Konfigurasi tambahan untuk schema.
        json_schema_extra digunakan untuk memberikan contoh di Swagger UI.
        """
        json_schema_extra = {
            "example": {
                "review_text": "This product is amazing! Great quality and fast shipping.",
                "product_name": "Wireless Headphones"
            }
        }


class SentimentResult(BaseModel):
    """
    Schema untuk hasil analisis sentimen.
    Digunakan sebagai bagian dari response atau untuk standalone sentiment API.
    """
    sentiment: str = Field(
        ...,  # Required
        description="Sentiment: positive, negative, or neutral"
    )
    """
    Hasil klasifikasi sentimen.
    Nilai yang mungkin: "positive", "negative", "neutral"
    """
    
    score: float = Field(
        ...,  # Required
        ge=0,  # Greater than or equal to 0
        le=1,  # Less than or equal to 1
        description="Confidence score between 0 and 1"
    )
    """
    Confidence score model AI (seberapa yakin model).
    Range: 0.0 - 1.0
    Contoh: 0.95 = model 95% yakin
    """


class KeyPointsResult(BaseModel):
    """
    Schema untuk hasil ekstraksi poin penting.
    Digunakan sebagai bagian dari response atau untuk standalone key points API.
    """
    key_points: List[str] = Field(
        ...,  # Required
        description="List of extracted key points"
    )
    """
    List berisi poin-poin penting dari review.
    
    Contoh:
        ["Kualitas produk excellent", "Pengiriman cepat", "Harga terjangkau"]
    """


class ReviewResponse(BaseModel):
    """
    Schema untuk response data review (beserta hasil analisis).
    Ini adalah representasi lengkap dari satu review di database.
    
    Digunakan untuk:
    - Response setelah analisis selesai
    - Response saat get review by ID
    - Item dalam list reviews
    """
    id: int
    """ID unik review di database"""
    
    review_text: str
    """Teks review asli dari user"""
    
    product_name: Optional[str] = None
    """Nama produk (jika ada)"""
    
    sentiment: Optional[str] = None
    """Hasil analisis sentimen: positive/negative/neutral"""
    
    sentiment_score: Optional[float] = None
    """Confidence score sentiment (0.0 - 1.0)"""
    
    key_points: Optional[List[str]] = None
    """List poin-poin penting hasil ekstraksi"""
    
    created_at: datetime
    """Timestamp kapan review dibuat"""
    
    updated_at: Optional[datetime] = None
    """Timestamp kapan review terakhir diupdate"""
    
    analysis_status: str
    """Status analisis: pending/processing/completed/partial/failed"""
    
    error_message: Optional[str] = None
    """Pesan error jika analisis gagal"""

    class Config:
        """
        Konfigurasi Pydantic.
        from_attributes=True memungkinkan Pydantic membaca data dari SQLAlchemy model.
        
        Contoh:
            review_db = db.query(Review).first()  # SQLAlchemy object
            review_response = ReviewResponse.from_orm(review_db)  # Pydantic object
        """
        from_attributes = True


class AnalysisResponse(BaseModel):
    """
    Schema untuk response API analisis review.
    Wrapper standar untuk response yang berisi status, message, dan data.
    
    Digunakan untuk:
    - POST /api/analyze-review
    - GET /api/reviews/{id}
    - DELETE /api/reviews/{id}
    """
    success: bool
    """
    Status apakah request berhasil.
    True = berhasil, False = gagal
    """
    
    message: str
    """
    Pesan human-readable tentang hasil operasi.
    Contoh: "Review analyzed successfully", "Review deleted"
    """
    
    data: Optional[ReviewResponse] = None
    """
    Data review (jika ada).
    None untuk operasi delete atau error.
    """


class ReviewListResponse(BaseModel):
    """
    Schema untuk response list reviews (dengan pagination).
    
    Digunakan untuk:
    - GET /api/reviews (with pagination and filter)
    """
    success: bool
    """Status apakah request berhasil"""
    
    total: int
    """
    Total jumlah reviews yang sesuai filter (untuk pagination).
    Berguna untuk menghitung jumlah halaman.
    
    Contoh:
        total = 100, limit = 10 -> ada 10 halaman
    """
    
    reviews: List[ReviewResponse]
    """
    List reviews pada halaman ini.
    Panjang list maksimal sesuai parameter 'limit' di query.
    """


class ErrorResponse(BaseModel):
    """
    Schema untuk response error standar.
    Digunakan saat terjadi error (4xx atau 5xx).
    
    Contoh error:
    - 400 Bad Request: Validation error
    - 404 Not Found: Review not found
    - 500 Internal Server Error: Unexpected error
    """
    success: bool = False
    """
    Status selalu False untuk error response.
    Default value = False
    """
    
    error: str
    """
    Tipe error atau pesan singkat.
    Contoh: "Validation Error", "Not Found", "Internal Server Error"
    """
    
    detail: Optional[str] = None
    """
    Detail lengkap error (opsional).
    Berguna untuk debugging.
    
    Contoh:
        error = "Validation Error"
        detail = "review_text: field required"
    """
