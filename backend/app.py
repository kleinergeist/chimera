import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
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


@app.get("/api/gosearch")
async def gosearch_proxy(username: str):
    """Proxy endpoint that calls the gosearch container's HTTP API.

    The gosearch service is expected at the hostname `gosearch` on port 8081
    in docker-compose. You can override the full URL via the GOSEARCH_URL env var.
    """
    if not username:
        raise HTTPException(status_code=400, detail="username query param is required")

    gosearch_url = os.getenv("GOSEARCH_URL", "http://gosearch:8081/search")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.get(gosearch_url, params={"username": username})
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"failed to reach gosearch service: {e}")

    # Proxy the JSON response (or an error) through
    try:
        data = resp.json()
    except Exception:
        # Non-JSON response: return raw text
        return JSONResponse(status_code=resp.status_code, content={"text": resp.text})

    return JSONResponse(status_code=resp.status_code, content=data)

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

@app.get("/api/accounts")
async def get_user_accounts(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Get all discovered accounts for the current user (Protected endpoint)"""
    user = get_current_user(user_info, db)
    
    # Get all sessions for this user
    sessions = db.query(DiagnosticSession).filter_by(user_id=user.id).all()
    session_ids = [s.id for s in sessions]
    
    # Get all accounts from user's sessions
    accounts = db.query(DiscoveredAccount).filter(DiscoveredAccount.session_id.in_(session_ids)).all()
    
    # Get assignments to know which bucket each account belongs to
    account_data = []
    for account in accounts:
        assignment = db.query(AccountAssignment).filter_by(account_id=account.id).first()
        bucket_info = None
        if assignment:
            bucket = db.query(UserBucket).filter_by(id=assignment.bucket_id).first()
            if bucket:
                bucket_info = {
                    "id": bucket.id,
                    "name": bucket.bucket_name
                }
        
        account_data.append({
            "id": account.id,
            "account_name": account.account_name,
            "email": account.email,
            "platform": account.platform,
            "metadata": account.account_metadata,
            "bucket": bucket_info,
            "created_at": account.created_at.isoformat() if account.created_at else None
        })
    
    return {
        "count": len(account_data),
        "accounts": account_data
    }

@app.put("/api/accounts/{account_id}/bucket")
async def update_account_bucket(
    account_id: int,
    bucket_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Update which bucket an account is assigned to"""
    user = get_current_user(user_info, db)
    bucket_id = bucket_data.get("bucket_id")
    
    # Verify account belongs to user's sessions
    sessions = db.query(DiagnosticSession).filter_by(user_id=user.id).all()
    session_ids = [s.id for s in sessions]
    account = db.query(DiscoveredAccount).filter(
        DiscoveredAccount.id == account_id,
        DiscoveredAccount.session_id.in_(session_ids)
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Find existing assignment
    assignment = db.query(AccountAssignment).filter_by(account_id=account_id).first()
    
    if bucket_id:
        # Verify bucket belongs to user
        bucket = db.query(UserBucket).filter_by(id=bucket_id, user_id=user.id).first()
        if not bucket:
            raise HTTPException(status_code=404, detail="Bucket not found")
        
        if assignment:
            assignment.bucket_id = bucket_id
        else:
            assignment = AccountAssignment(
                account_id=account_id,
                bucket_id=bucket_id
            )
            db.add(assignment)
    else:
        # Remove assignment if bucket_id is None
        if assignment:
            db.delete(assignment)
    
    db.commit()
    return {"message": "Account bucket updated"}

@app.post("/api/buckets")
async def create_bucket(
    bucket_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Create a new bucket"""
    user = get_current_user(user_info, db)
    
    bucket_name = bucket_data.get("bucket_name")
    description = bucket_data.get("description", "")
    
    if not bucket_name:
        raise HTTPException(status_code=400, detail="Bucket name is required")
    
    new_bucket = UserBucket(
        user_id=user.id,
        bucket_name=bucket_name,
        description=description
    )
    db.add(new_bucket)
    db.commit()
    db.refresh(new_bucket)
    
    return {
        "id": new_bucket.id,
        "bucket_name": new_bucket.bucket_name,
        "description": new_bucket.description
    }

@app.delete("/api/buckets/{bucket_id}")
async def delete_bucket(
    bucket_id: int,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Delete a bucket"""
    user = get_current_user(user_info, db)
    
    bucket = db.query(UserBucket).filter_by(id=bucket_id, user_id=user.id).first()
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    # Delete associated assignments
    db.query(AccountAssignment).filter_by(bucket_id=bucket_id).delete()
    
    db.delete(bucket)
    db.commit()
    
    return {"message": "Bucket deleted"}
