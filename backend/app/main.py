"""
FastAPI Main Application
File entry point utama untuk menjalankan backend API.
Mendefinisikan aplikasi FastAPI, middleware, dan lifecycle events.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routes import router

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
"""
Setup logging untuk tracking aplikasi.
Log akan ditampilkan di console dengan format:
    2024-01-15 10:30:00 - app.main - INFO - Starting up application...
"""
logging.basicConfig(
    level=logging.INFO,  # Level log: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==========================================
# APPLICATION LIFECYCLE EVENTS
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Mengelola lifecycle aplikasi (startup dan shutdown).
    
    Lifespan events:
    1. STARTUP (before yield):
       - Inisialisasi database (buat tabel jika belum ada)
       - Load model AI (jika diperlukan)
       - Setup koneksi ke external services
       
    2. SHUTDOWN (after yield):
       - Cleanup resources
       - Close connections
       - Save state jika diperlukan
    
    Ini adalah pattern modern FastAPI (menggantikan @app.on_event).
    """
    # ==========================================
    # STARTUP PHASE
    # ==========================================
    logger.info("Starting up application...")
    try:
        # Inisialisasi database (buat tabel jika belum ada)
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        logger.warning("Application will continue, but database operations may fail")
        # Tidak raise error agar aplikasi tetap jalan (untuk debugging)
    
    yield  # Yield berarti "aplikasi running di sini"
    
    # ==========================================
    # SHUTDOWN PHASE
    # ==========================================
    logger.info("Shutting down application...")
    # Cleanup tasks bisa ditambahkan di sini jika diperlukan


# ==========================================
# FASTAPI APPLICATION INSTANCE
# ==========================================
"""
Membuat instance aplikasi FastAPI dengan konfigurasi.
"""
app = FastAPI(
    title="Product Review Analyzer API",
    description="""
    A powerful API for analyzing product reviews using AI.
    
    ## Features
    
    * **Sentiment Analysis** - Analyze review sentiment using Hugging Face models
    * **Key Points Extraction** - Extract important points using Google Gemini
    * **Database Storage** - Store and retrieve analysis results
    
    ## Endpoints
    
    * `POST /api/analyze-review` - Analyze a new review
    * `GET /api/reviews` - Get all reviews with pagination
    * `GET /api/reviews/{id}` - Get a specific review
    * `DELETE /api/reviews/{id}` - Delete a review
    """,
    version="1.0.0",
    lifespan=lifespan,  # Gunakan lifespan manager di atas
    docs_url="/docs",   # Swagger UI URL
    redoc_url="/redoc"  # ReDoc URL (alternatif documentation)
)

# ==========================================
# CORS MIDDLEWARE
# ==========================================
"""
CORS (Cross-Origin Resource Sharing) Middleware.

CORS adalah security mechanism browser yang mencegah website berbahaya
mengakses API kita. Kita perlu explicitly mengizinkan origin tertentu.

Configurasi:
- allow_origins: List domain frontend yang boleh akses API
- allow_credentials: Izinkan cookies/auth headers
- allow_methods: HTTP methods yang diizinkan (GET, POST, dll)
- allow_headers: HTTP headers yang diizinkan

Tanpa CORS, browser akan block request dari frontend ke backend.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Frontend domains yang diizinkan
    allow_credentials=True,  # Izinkan credentials (cookies, auth headers)
    allow_methods=["*"],     # Izinkan semua HTTP methods (GET, POST, PUT, DELETE, dll)
    allow_headers=["*"],     # Izinkan semua headers
)

# ==========================================
# INCLUDE ROUTERS
# ==========================================
"""
Include router dari routes.py.
Router berisi semua endpoint API (/api/analyze-review, /api/reviews, dll).
"""
app.include_router(router)


# ==========================================
# ROOT ENDPOINT
# ==========================================
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API health check dan informasi API.
    
    Endpoint ini bisa diakses di http://localhost:8000/
    Berguna untuk:
    - Cek apakah API running
    - Melihat info dasar API
    - Redirect ke documentation
    
    Returns:
        dict: Informasi API dan link ke documentation
    """
    return {
        "status": "healthy",
        "message": "Product Review Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"  # Link ke Swagger UI
    }


# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint untuk monitoring.
    
    Berguna untuk:
    - Load balancer health checks
    - Uptime monitoring services
    - Container orchestration (Kubernetes, Docker Swarm)
    
    Returns:
        dict: Status aplikasi
    """
    return {
        "status": "healthy",
        "service": "review-analyzer-api"
    }


# ==========================================
# GLOBAL EXCEPTION HANDLER
# ==========================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler untuk menangkap semua unhandled errors.
    
    Jika ada error yang tidak di-handle di route manapun,
    error akan ditangkap di sini dan dikonversi jadi response JSON.
    
    Keuntungan:
    - Mencegah aplikasi crash
    - Memberikan response error yang konsisten
    - Logging error untuk debugging
    
    Args:
        request: FastAPI Request object
        exc: Exception yang terjadi
        
    Returns:
        JSONResponse: Error response dalam format standar
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,  # Internal Server Error
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)  # Detail error (untuk debugging)
        }
    )


# ==========================================
# DIRECT RUN (Development Only)
# ==========================================
if __name__ == "__main__":
    """
    Jalankan server jika file ini dieksekusi langsung.
    
    Penggunaan:
        python -m app.main
        
    Untuk production, gunakan uvicorn directly:
        uvicorn app.main:app --host 0.0.0.0 --port 8000
        
    atau gunakan run.py yang sudah disediakan.
    """
    import uvicorn
    uvicorn.run(
        "app.main:app",         # Application path
        host=settings.HOST,      # Host dari config
        port=settings.PORT,      # Port dari config
        reload=True              # Auto-reload saat file berubah (development only)
    )
