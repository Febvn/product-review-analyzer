"""
Database Models (ORM Models)
File ini mendefinisikan struktur tabel database menggunakan SQLAlchemy ORM.
ORM = Object Relational Mapping (mengubah tabel database jadi class Python).
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from app.database import Base


class Review(Base):
    """
    Model untuk tabel 'reviews' di database.
    Menyimpan data review produk dan hasil analisis AI.
    
    Struktur tabel:
    - id: Primary key (auto-increment)
    - review_text: Teks review dari user
    - product_name: Nama produk (opsional)
    - sentiment: Hasil analisis sentimen (positive/negative/neutral)
    - sentiment_score: Confidence score dari model AI (0.0 - 1.0)
    - key_points: List poin-poin penting (disimpan sebagai JSON)
    - created_at: Timestamp kapan review dibuat
    - updated_at: Timestamp kapan review terakhir diupdate
    - analysis_status: Status proses analisis (pending/completed/failed)
    - error_message: Pesan error jika analisis gagal
    """
    
    # Nama tabel di database
    __tablename__ = "reviews"

    # ==========================================
    # PRIMARY KEY
    # ==========================================
    id = Column(
        Integer,           # Tipe data integer
        primary_key=True,  # Ini adalah primary key
        index=True,        # Buat index untuk query lebih cepat
        autoincrement=True # Auto increment (1, 2, 3, ...)
    )
    
    # ==========================================
    # DATA REVIEW (Input dari User)
    # ==========================================
    review_text = Column(
        Text,              # Tipe data text (unlimited length)
        nullable=False     # Wajib diisi (tidak boleh NULL)
    )
    """
    Teks review yang diinput oleh user.
    Contoh: "Produk ini sangat bagus, pengiriman cepat dan packing rapi."
    """
    
    product_name = Column(
        String(255),       # Tipe data string dengan max 255 karakter
        nullable=True      # Opsional (boleh NULL)
    )
    """
    Nama produk yang di-review (opsional).
    Contoh: "Laptop ASUS ROG", "Samsung Galaxy S23"
    """
    
    # ==========================================
    # HASIL ANALISIS SENTIMEN
    # ==========================================
    sentiment = Column(
        String(50),        # Tipe data string dengan max 50 karakter
        nullable=True      # Boleh NULL (akan diisi setelah analisis selesai)
    )
    """
    Hasil klasifikasi sentimen dari model AI.
    Nilai yang mungkin: 'positive', 'negative', 'neutral'
    """
    
    sentiment_score = Column(
        Float,             # Tipe data float (desimal)
        nullable=True      # Boleh NULL
    )
    """
    Confidence score dari model (seberapa yakin model dengan prediksi).
    Range: 0.0 - 1.0
    Contoh: 0.95 = model 95% yakin review ini positive
    """
    
    # ==========================================
    # HASIL EKSTRAKSI POIN PENTING
    # ==========================================
    key_points = Column(
        JSON,              # Tipe data JSON (bisa simpan list/dictionary)
        nullable=True      # Boleh NULL
    )
    """
    List poin-poin penting yang diekstrak dari review.
    Disimpan sebagai JSON array.
    
    Contoh:
        ["Kualitas produk excellent", "Pengiriman sangat cepat", "Harga terjangkau"]
    """
    
    # ==========================================
    # METADATA (Informasi Tambahan)
    # ==========================================
    created_at = Column(
        DateTime,                  # Tipe data datetime
        default=datetime.utcnow,   # Default value = waktu sekarang (UTC)
        nullable=False             # Wajib ada
    )
    """
    Timestamp kapan record ini dibuat.
    Otomatis diisi dengan waktu sekarang saat insert.
    """
    
    updated_at = Column(
        DateTime,                      # Tipe data datetime
        default=datetime.utcnow,       # Default value = waktu sekarang
        onupdate=datetime.utcnow       # Auto-update saat record di-update
    )
    """
    Timestamp kapan record ini terakhir diupdate.
    Otomatis di-update setiap kali ada perubahan data.
    """
    
    # ==========================================
    # STATUS TRACKING
    # ==========================================
    analysis_status = Column(
        String(50),
        default="pending"  # Default status adalah "pending"
    )
    """
    Status proses analisis.
    
    Nilai yang mungkin:
    - "pending": Belum diproses
    - "processing": Sedang dianalisis
    - "completed": Analisis berhasil
    - "partial": Analisis sebagian berhasil (misalnya sentiment berhasil, tapi key points gagal)
    - "failed": Analisis gagal
    """
    
    error_message = Column(
        Text,              # Tipe data text
        nullable=True      # Boleh NULL
    )
    """
    Pesan error jika analisis gagal.
    Berguna untuk debugging.
    Contoh: "Gemini API rate limit exceeded"
    """

    def __repr__(self):
        """
        Representasi string dari object (untuk debugging).
        Dipanggil saat print(review_object).
        
        Contoh output:
            <Review(id=1, sentiment=positive)>
        """
        return f"<Review(id={self.id}, sentiment={self.sentiment})>"
    
    def to_dict(self):
        """
        Konversi model object menjadi dictionary.
        Berguna untuk serialisasi ke JSON response.
        
        Returns:
            dict: Dictionary berisi semua field model
            
        Contoh:
            review = db.query(Review).first()
            review_dict = review.to_dict()  # Jadi dictionary
            
        Output:
            {
                "id": 1,
                "review_text": "Produk bagus!",
                "product_name": "Laptop ASUS",
                "sentiment": "positive",
                "sentiment_score": 0.95,
                "key_points": ["Kualitas bagus", "Harga terjangkau"],
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "analysis_status": "completed",
                "error_message": null
            }
        """
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
