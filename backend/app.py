import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, DiagnosticSession, DiscoveredAccount, UserBucket, AccountAssignment
from auth import get_current_user, get_clerk_user_id

app = FastAPI(title="Chimera API", version="1.0.0")

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_USER = os.getenv('POSTGRES_USER', 'chimera_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'chimera_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'chimera_db')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Chimera API is running"}

@app.get("/api/users/me")
async def get_current_user_info(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Get current authenticated user info (Protected endpoint)"""
    user = get_current_user(user_info, db)
    
    return {
        "id": user.id,
        "clerk_id": user.clerk_id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@app.get("/api/sessions")
async def get_user_sessions(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Get all diagnostic sessions for the current user (Protected endpoint)"""
    user = get_current_user(user_info, db)
    
    sessions = db.query(DiagnosticSession).filter_by(user_id=user.id).all()
    
    return {
        "count": len(sessions),
        "sessions": [
            {
                "id": session.id,
                "status": session.status,
                "created_at": session.created_at.isoformat() if session.created_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None
            }
            for session in sessions
        ]
    }

@app.get("/api/buckets")
async def get_user_buckets(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Get all buckets for the current user (Protected endpoint)"""
    user = get_current_user(user_info, db)
    
    buckets = db.query(UserBucket).filter_by(user_id=user.id).all()
    
    return {
        "count": len(buckets),
        "buckets": [
            {
                "id": bucket.id,
                "bucket_name": bucket.bucket_name,
                "description": bucket.description,
                "created_at": bucket.created_at.isoformat() if bucket.created_at else None
            }
            for bucket in buckets
        ]
    }
