"""
FastAPI Main Application
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up application...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        logger.warning("Application will continue, but database operations may fail")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
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
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "message": "Product Review Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "review-analyzer-api"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
