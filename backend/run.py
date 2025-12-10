"""
Run script for the FastAPI backend server.
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 50)
    print("  Product Review Analyzer API")
    print("=" * 50)
    print(f"  Server: http://{settings.HOST}:{settings.PORT}")
    print(f"  Docs:   http://localhost:{settings.PORT}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )
