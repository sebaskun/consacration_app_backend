from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import auth_router, users_router, content_router
from app.database import engine, Base
import uvicorn
import uuid

# Create database tables
# Base.metadata.create_all(bind=engine)

# Load daily content if database is empty
def load_initial_data():
    """Load initial data if database is empty"""
    try:
        from sqlalchemy.orm import Session
        from app.models.content import DailyContent
        from app.database import SessionLocal
        import json
        import os
        
        db = SessionLocal()
        try:
            # Check if daily content exists
            existing_content = db.query(DailyContent).first()
            if not existing_content:
                # Load from JSON file
                json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "daily_content.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r', encoding='utf-8') as file:
                        content_data = json.load(file)
                    
                    for day_data in content_data:
                        content = DailyContent(**day_data)
                        db.add(content)
                    
                    db.commit()
                    print(f"✅ Loaded {len(content_data)} days of content into database")
        except Exception as e:
            print(f"⚠️  Could not load initial data: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️  Error in load_initial_data: {e}")

# Load initial data
load_initial_data()

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="API para la aplicación de consagración total a María",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom CORS origin checker for Vercel preview deployments
def is_cors_allowed(origin: str) -> bool:
    allowed_origins = settings.backend_cors_origins
    
    # Check exact matches first
    if origin in allowed_origins:
        return True
    
    # Allow Vercel preview deployments (consacration-app-frontend-*.vercel.app)
    if origin and origin.startswith("https://consacration-app-frontend-") and origin.endswith(".vercel.app"):
        return True
    
    return False

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://consacration-app-frontend.*\.vercel\.app",
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.api_v1_str)
app.include_router(users_router, prefix=settings.api_v1_str)
app.include_router(content_router, prefix=settings.api_v1_str)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Totus Tuus - App de Consagración Total",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 