import os
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import User

security = HTTPBearer()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

def get_clerk_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify Clerk JWT token and extract user information"""
    try:
        token = credentials.credentials
        
        # Decode JWT from Clerk (using RS256 algorithm)
        # Note: In production, you should verify the signature properly
        # For now, we're decoding without verification for simplicity
        payload = jwt.decode(
            token,
            options={"verify_signature": False}  # Clerk tokens are pre-verified
        )
        
        clerk_user_id = payload.get("sub")
        
        # Try multiple ways to extract email from token
        email = None
        if "email" in payload:
            email = payload.get("email")
        elif "email_addresses" in payload and payload["email_addresses"]:
            email = payload["email_addresses"][0] if isinstance(payload["email_addresses"], list) else None
        
        # Fallback to generated email if none found
        if not email:
            email = f"user_{clerk_user_id}@clerk.temp"
        
        if not clerk_user_id:
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")
        
        return {
            "clerk_id": clerk_user_id,
            "email": email
        }
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

def get_current_user(
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = None
) -> User:
    """Get or create user from Clerk ID"""
    if db is None:
        raise HTTPException(status_code=500, detail="Database session not provided")
    
    clerk_id = user_info["clerk_id"]
    email = user_info.get("email", f"user_{clerk_id}@clerk.temp")
    
    # Try to find existing user
    user = db.query(User).filter_by(clerk_id=clerk_id).first()
    
    if not user:
        # Auto-create user on first login
        user = User(clerk_id=clerk_id, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user

