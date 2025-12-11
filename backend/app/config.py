"""
Konfigurasi Aplikasi
File ini mengelola semua pengaturan environment variable untuk aplikasi.
Environment variables dimuat dari file .env di root folder backend.
"""
import os
from dotenv import load_dotenv

# Muat environment variables dari file .env
# File .env harus berada di root folder backend (sejajar dengan run.py)
load_dotenv()

class Settings:
    """
    Kelas untuk menyimpan semua pengaturan aplikasi.
    Semua nilai diambil dari environment variables dengan fallback ke default value.
    
    Cara menggunakan:
        from app.config import settings
        print(settings.DATABASE_URL)
    """
    
    # ==========================================
    # KONFIGURASI DATABASE
    # ==========================================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",  # Nama environment variable
        "postgresql://postgres:postgres@localhost:5432/review_analyzer"  # Default jika tidak ada di .env
    )
    """
    URL koneksi database untuk PostgreSQL atau SQLite.
    
    Format PostgreSQL: postgresql://username:password@host:port/database_name
    Format SQLite: sqlite:///./review_analyzer.db
    
    Contoh:
        PostgreSQL: postgresql://postgres:mypassword@localhost:5432/review_analyzer
        SQLite: sqlite:///./review_analyzer.db
    """
    
    # ==========================================
    # KONFIGURASI AI/ML SERVICES
    # ==========================================
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    """
    API Key untuk Hugging Face Hub (opsional).
    Tidak wajib karena kita menggunakan model lokal yang di-download otomatis.
    Hanya diperlukan jika ingin akses model private atau rate limit lebih tinggi.
    """
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    """
    API Key untuk Google Gemini AI (untuk ekstraksi key points).
    
    Cara mendapatkan:
    1. Buka https://makersuite.google.com/app/apikey
    2. Login dengan Google Account
    3. Buat API Key baru
    4. Copy dan paste ke file .env
    
    Jika tidak tersedia, aplikasi akan menggunakan fallback method NLP sederhana.
    """
    
    # ==========================================
    # KONFIGURASI SERVER
    # ==========================================
    HOST: str = os.getenv("HOST", "0.0.0.0")
    """
    Host address untuk menjalankan server.
    
    - "0.0.0.0" = Bisa diakses dari network lain (production)
    - "127.0.0.1" = Hanya bisa diakses dari localhost (lebih aman untuk development)
    """
    
    PORT: int = int(os.getenv("PORT", "8000"))
    """
    Port number untuk menjalankan server.
    Default 8000, bisa diganti jika port sudah digunakan aplikasi lain.
    """
    
    # ==========================================
    # KONFIGURASI CORS (Cross-Origin Resource Sharing)
    # ==========================================
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",   # Vite dev server default port
        "http://localhost:3000",   # Create React App / Next.js default port
        "http://127.0.0.1:5173",   # Alternatif localhost
        "http://127.0.0.1:3000",   # Alternatif localhost
    ]
    """
    Daftar origin (frontend URL) yang diizinkan untuk mengakses API.
    
    CORS adalah security mechanism di browser untuk mencegah website berbahaya
    mengakses API kita. Hanya frontend dari URL di list ini yang bisa hit API.
    
    Untuk production, tambahkan domain deployment Anda:
        "https://your-app.vercel.app",
        "https://your-app.netlify.app",
    """

# ==========================================
# SINGLETON INSTANCE
# ==========================================
# Instance global settings yang bisa diimport di seluruh aplikasi
# Penggunaan: from app.config import settings
settings = Settings()
