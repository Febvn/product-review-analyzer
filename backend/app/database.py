"""
Konfigurasi Database dan Session Management
File ini mengelola koneksi ke database dan menyediakan session untuk operasi database.
Mendukung PostgreSQL (production) dan SQLite (development).
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# ==========================================
# SETUP DATABASE CONNECTION
# ==========================================

# Ambil URL database dari settings (bisa PostgreSQL atau SQLite)
database_url = settings.DATABASE_URL

# Tentukan jenis database dan buat engine yang sesuai
if database_url.startswith("sqlite"):
    # ==========================================
    # KONFIGURASI SQLite (untuk Development)
    # ==========================================
    """
    SQLite adalah database file-based yang ringan, cocok untuk development/testing.
    Tidak perlu install server terpisah, data disimpan dalam satu file .db.
    """
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Diperlukan untuk SQLite agar bisa digunakan multi-thread
        echo=False  # Set True untuk melihat SQL query di console (debugging)
    )
    print("Using SQLite database")
else:
    # ==========================================
    # KONFIGURASI PostgreSQL (untuk Production)
    # ==========================================
    """
    PostgreSQL adalah database server yang powerful, cocok untuk production.
    Memerlukan PostgreSQL server yang sudah running.
    """
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # Cek koneksi sebelum digunakan (mencegah "connection lost")
        pool_recycle=300,    # Recycle koneksi setiap 5 menit (mencegah stale connections)
        echo=False           # Set True untuk debugging SQL queries
    )
    print("Using PostgreSQL database")

# ==========================================
# SESSION FACTORY
# ==========================================
"""
SessionLocal adalah factory untuk membuat database session.
Session digunakan untuk melakukan operasi database (query, insert, update, delete).

Parameter:
- autocommit=False: Perubahan tidak langsung di-commit, harus manual commit()
- autoflush=False: Perubahan tidak otomatis di-flush ke database
- bind=engine: Gunakan engine yang sudah dibuat di atas
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==========================================
# BASE CLASS untuk Model
# ==========================================
"""
Base adalah parent class untuk semua database model.
Semua model (seperti Review) harus inherit dari Base ini.

Fungsi:
- Menyediakan metadata untuk membuat tabel
- Menyediakan mekanisme ORM (Object Relational Mapping)
"""
Base = declarative_base()


def get_db():
    """
    Dependency Injection untuk mendapatkan database session.
    Fungsi ini digunakan di FastAPI route dengan Depends(get_db).
    
    Cara kerja:
    1. Membuat session baru
    2. Yield session ke route (route bisa pakai session untuk query)
    3. Setelah route selesai, session otomatis di-close (cleanup)
    
    Contoh penggunaan di route:
        @app.get("/reviews")
        def get_reviews(db: Session = Depends(get_db)):
            reviews = db.query(Review).all()
            return reviews
    
    Pattern ini memastikan:
    - Session selalu fresh untuk setiap request
    - Session otomatis di-close setelah request selesai
    - Tidak ada connection leak
    """
    db = SessionLocal()
    try:
        yield db  # Berikan session ke route yang memanggilnya
    finally:
        db.close()  # Pastikan session di-close setelah selesai


def init_db():
    """
    Inisialisasi database dengan membuat semua tabel.
    Fungsi ini dipanggil saat aplikasi startup (lihat main.py).
    
    Cara kerja:
    1. Import semua models (agar Base.metadata tahu tabel apa saja yang perlu dibuat)
    2. Panggil create_all() untuk membuat tabel di database
    
    PENTING:
    - Fungsi ini hanya membuat tabel yang belum ada
    - Tidak akan menghapus data yang sudah ada
    - Tidak akan mengubah struktur tabel yang sudah ada (untuk itu perlu migration)
    
    Untuk production, sebaiknya gunakan Alembic untuk database migration.
    """
    from app import models  # noqa: F401  # Import models agar terdaftar
    Base.metadata.create_all(bind=engine)  # Buat semua tabel di database
    print("Database tables created successfully")
