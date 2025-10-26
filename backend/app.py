import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, DiagnosticSession, DiscoveredAccount, UserBucket, AccountAssignment
from auth import get_current_user, get_clerk_user_id
from openai import OpenAI

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

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    
    # Ensure "Unassigned" bucket exists for this user
    unassigned_bucket = db.query(UserBucket).filter_by(
        user_id=user.id, 
        bucket_name="Unassigned"
    ).first()
    
    if not unassigned_bucket:
        unassigned_bucket = UserBucket(
            user_id=user.id,
            bucket_name="Unassigned",
            description="Default bucket for accounts that haven't been assigned to a persona"
        )
        db.add(unassigned_bucket)
        db.commit()
        db.refresh(unassigned_bucket)
        buckets.append(unassigned_bucket)
    
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
        
        # Parse metadata to get URL
        url = None
        if account.account_metadata:
            try:
                metadata = json.loads(account.account_metadata)
                url = metadata.get("url")
            except:
                pass
        
        account_data.append({
            "id": account.id,
            "account_name": account.account_name,
            "email": account.email,
            "platform": account.platform,
            "url": url,
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

@app.put("/api/buckets/{bucket_id}")
async def update_bucket(
    bucket_id: int,
    bucket_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Update a bucket's name and/or description"""
    user = get_current_user(user_info, db)
    
    bucket = db.query(UserBucket).filter_by(id=bucket_id, user_id=user.id).first()
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    
    # Prevent renaming "Unassigned" bucket
    if bucket.bucket_name.lower().strip() == "unassigned":
        raise HTTPException(status_code=400, detail="Cannot rename the 'Unassigned' bucket. This is a system bucket.")
    
    # Update fields if provided
    if "bucket_name" in bucket_data and bucket_data["bucket_name"]:
        bucket.bucket_name = bucket_data["bucket_name"]
    if "description" in bucket_data:
        bucket.description = bucket_data["description"]
    
    db.commit()
    db.refresh(bucket)
    
    return {
        "id": bucket.id,
        "bucket_name": bucket.bucket_name,
        "description": bucket.description
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
    
    # Prevent deletion of "Unassigned" bucket
    if bucket.bucket_name.lower().strip() == "unassigned":
        raise HTTPException(status_code=400, detail="Cannot delete the 'Unassigned' bucket. This is a system bucket.")
    
    # Delete associated assignments
    db.query(AccountAssignment).filter_by(bucket_id=bucket_id).delete()
    
    db.delete(bucket)
    db.commit()
    
    return {"message": "Bucket deleted"}

@app.post("/api/search-accounts")
async def search_and_save_accounts(
    search_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Search for accounts using gosearch and save to discovered_accounts"""
    user = get_current_user(user_info, db)
    username = search_data.get("username")
    
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    # Call gosearch service
    gosearch_url = os.getenv("GOSEARCH_URL", "http://gosearch:8081/search")
    
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.get(gosearch_url, params={"username": username})
            resp.raise_for_status()
            gosearch_data = resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Failed to reach gosearch service: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling gosearch: {e}")
    
    # Create a new diagnostic session for this search
    session = DiagnosticSession(
        user_id=user.id,
        status="completed"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Parse and save discovered accounts
    platforms = gosearch_data.get("platforms", [])
    saved_count = 0
    
    for platform in platforms:
        if platform.get("found"):
            # Check if this account already exists for this user
            existing = db.query(DiscoveredAccount).join(DiagnosticSession).filter(
                DiagnosticSession.user_id == user.id,
                DiscoveredAccount.platform == platform["name"],
                DiscoveredAccount.account_name == username
            ).first()
            
            if not existing:
                account = DiscoveredAccount(
                    session_id=session.id,
                    account_name=username,
                    email=None,  # gosearch doesn't provide email
                    platform=platform["name"],
                    account_metadata=json.dumps({"url": platform["url"]})
                )
                db.add(account)
                saved_count += 1
    
    db.commit()
    
    return {
        "message": "Search completed",
        "username": username,
        "total_found": len(platforms),
        "new_accounts_saved": saved_count,
        "session_id": session.id
    }

@app.post("/api/generate-summary")
async def generate_summary(
    request_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Generate an AI summary of the user's discovered accounts based on websites only"""
    user = get_current_user(user_info, db)
    
    # Get all sessions for this user
    sessions = db.query(DiagnosticSession).filter_by(user_id=user.id).all()
    session_ids = [s.id for s in sessions]
    
    # Get all accounts from user's sessions
    accounts = db.query(DiscoveredAccount).filter(DiscoveredAccount.session_id.in_(session_ids)).all()
    
    # Filter by bucket if specified
    bucket_id = request_data.get("bucket_id")
    bucket_name = None
    if bucket_id:
        # Get accounts assigned to this specific bucket
        assignments = db.query(AccountAssignment).filter_by(bucket_id=bucket_id).all()
        assigned_account_ids = [a.account_id for a in assignments]
        accounts = [acc for acc in accounts if acc.id in assigned_account_ids]
        
        # Get bucket name for context
        bucket = db.query(UserBucket).filter_by(id=bucket_id).first()
        if bucket:
            bucket_name = bucket.bucket_name
    
    if not accounts:
        context = f"in the {bucket_name} persona" if bucket_name else ""
        return {"summary": f"No accounts found {context} to generate summary."}
    
    
    # Prepare account data for OpenAI - only platform names
    platform_names = []
    for account in accounts:
        platform_names.append(account.platform)
    
    # Create prompt for OpenAI
    persona_context = f" within the {bucket_name} persona" if bucket_name else ""
    prompt = f"""Analyze the following platforms{persona_context} and create a concise, formatted summary. Focus on: 1) What types of accounts exist, 2) What kind of person this reveals, 3) Privacy assessment.

Platforms: {', '.join(platform_names)}

Format your response as:
**Profile Overview:** [2-3 sentences describing the person based on platform types]

**Account Categories:**
• [Category 1]: [platforms]
• [Category 2]: [platforms]

**Privacy Assessment:** [2-3 sentences evaluating privacy. If platforms are all within the same life area (all professional, all creative, all gaming, etc.), this is GOOD for privacy - praise the separation. If platforms mix different life areas (e.g., work + gaming, professional + creative), warn about identity leakage risks from cross-referencing.]

Keep it concise but insightful. Do NOT mention usernames or account names - only platform types."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a digital privacy analyst. Create concise, well-formatted summaries. When platforms are well-separated within a single life area, give POSITIVE privacy assessments. When platforms mix different life areas, warn about identity leakage. Use markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        
        return {
            "summary": summary,
            "account_count": len(accounts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@app.post("/api/split-personas")
async def split_personas(
    request_data: dict,
    user_info: dict = Depends(get_clerk_user_id),
    db: Session = Depends(get_db)
):
    """Split discovered accounts into separate personas based on platform categories"""
    user = get_current_user(user_info, db)
    
    # Get all sessions for this user
    sessions = db.query(DiagnosticSession).filter_by(user_id=user.id).all()
    session_ids = [s.id for s in sessions]
    
    # Get all accounts from user's sessions
    accounts = db.query(DiscoveredAccount).filter(DiscoveredAccount.session_id.in_(session_ids)).all()
    
    # Filter by bucket if specified
    bucket_id = request_data.get("bucket_id")
    bucket_name = None
    if bucket_id:
        # Get accounts assigned to this specific bucket
        assignments = db.query(AccountAssignment).filter_by(bucket_id=bucket_id).all()
        assigned_account_ids = [a.account_id for a in assignments]
        accounts = [acc for acc in accounts if acc.id in assigned_account_ids]
        
        # Get bucket name for context
        bucket = db.query(UserBucket).filter_by(id=bucket_id).first()
        if bucket:
            bucket_name = bucket.bucket_name
    
    if not accounts:
        context = f"in the {bucket_name} persona" if bucket_name else ""
        return {"message": f"No accounts found {context} to split into personas."}
    
    # Prepare platform data for OpenAI categorization
    platform_names = [account.platform for account in accounts]
    
    # Create prompt for OpenAI to categorize platforms into personas
    prompt = f"""Based on the following platforms, categorize them into STRICTLY SEPARATED digital personas to prevent identity leakage. Each persona must represent a completely distinct life area with NO overlap.

Platforms found:
{', '.join(platform_names)}

STRICT CATEGORIZATION RULES:
- **Professional**: ONLY work/career platforms (LinkedIn, GitHub for work, Slack, Microsoft Teams, professional networking)
- **Creative**: ONLY artistic/creative platforms (DeviantArt, AO3, Behance, Dribbble, art portfolios, fanfiction)
- **Gaming**: ONLY gaming platforms (Steam, Xbox, PlayStation, Twitch, Discord gaming servers, gaming communities)
- **Social/Personal**: ONLY personal social media (Facebook, Instagram, Twitter/X, TikTok, personal blogs)
- **Academic/Educational**: ONLY learning/education platforms (Coursera, edX, academic journals, university portals)
- **Financial**: ONLY financial platforms (banking, PayPal, Venmo, crypto exchanges, investment apps)

CRITICAL RULES:
1. You MUST categorize EVERY platform - no exceptions
2. Each platform goes to EXACTLY ONE persona
3. NEVER mix life areas (e.g., NO Twitch in Professional, NO LinkedIn in Gaming, NO Steam in Creative)
4. If uncertain, choose the persona that matches the platform's PRIMARY purpose
5. Keep professional life completely separate from gaming/creative/personal

Return a JSON response with this structure:
{{
    "personas": [
        {{
            "name": "Professional",
            "description": "Work and career-related platforms",
            "platforms": ["LinkedIn", "GitHub"]
        }},
        {{
            "name": "Creative",
            "description": "Artistic and creative expression platforms",
            "platforms": ["DeviantArt", "AO3"]
        }}
    ]
}}

Ensure platforms are distributed logically to prevent cross-persona contamination."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a digital privacy expert. Categorize platforms into separate personas to minimize identity leakage. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        # Parse the JSON response
        import re
        json_match = re.search(r'\{.*\}', response.choices[0].message.content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in response")
        
        personas_data = json.loads(json_match.group())
        personas = personas_data.get("personas", [])
        
        # Create buckets for each persona
        created_buckets = []
        for persona in personas:
            # Check if bucket already exists
            existing_bucket = db.query(UserBucket).filter_by(
                user_id=user.id,
                bucket_name=persona["name"]
            ).first()
            
            if not existing_bucket:
                bucket = UserBucket(
                    user_id=user.id,
                    bucket_name=persona["name"],
                    description=persona["description"]
                )
                db.add(bucket)
                db.commit()
                db.refresh(bucket)
                created_buckets.append(bucket)
            else:
                created_buckets.append(existing_bucket)
        
        # Assign accounts to appropriate buckets
        assigned_count = 0
        assigned_platforms = set()
        
        for persona in personas:
            bucket = next((b for b in created_buckets if b.bucket_name == persona["name"]), None)
            if not bucket:
                continue
                
            for platform_name in persona["platforms"]:
                assigned_platforms.add(platform_name)
                # Find accounts with this platform
                matching_accounts = [acc for acc in accounts if acc.platform == platform_name]
                
                for account in matching_accounts:
                    # Check if already assigned
                    existing_assignment = db.query(AccountAssignment).filter_by(account_id=account.id).first()
                    
                    if existing_assignment:
                        # Update existing assignment to new bucket
                        existing_assignment.bucket_id = bucket.id
                        assigned_count += 1
                    else:
                        # Create new assignment
                        assignment = AccountAssignment(
                            account_id=account.id,
                            bucket_id=bucket.id
                        )
                        db.add(assignment)
                        assigned_count += 1
        
        # Handle any platforms that weren't categorized by AI (fallback to Social/Personal)
        uncategorized_platforms = set(platform_names) - assigned_platforms
        if uncategorized_platforms:
            # Find or create Social/Personal bucket for leftovers
            social_bucket = next((b for b in created_buckets if b.bucket_name == "Social/Personal"), None)
            if not social_bucket:
                social_bucket = UserBucket(
                    user_id=user.id,
                    bucket_name="Social/Personal",
                    description="Personal and social platforms"
                )
                db.add(social_bucket)
                db.commit()
                db.refresh(social_bucket)
            
            for platform_name in uncategorized_platforms:
                matching_accounts = [acc for acc in accounts if acc.platform == platform_name]
                for account in matching_accounts:
                    existing_assignment = db.query(AccountAssignment).filter_by(account_id=account.id).first()
                    if existing_assignment:
                        # Update existing assignment to Social/Personal bucket
                        existing_assignment.bucket_id = social_bucket.id
                        assigned_count += 1
                    else:
                        # Create new assignment
                        assignment = AccountAssignment(
                            account_id=account.id,
                            bucket_id=social_bucket.id
                        )
                        db.add(assignment)
                        assigned_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully split accounts into {len(personas)} personas",
            "personas": personas,
            "buckets_created": len([b for b in created_buckets if b.id]),
            "accounts_assigned": assigned_count,
            "uncategorized_handled": len(uncategorized_platforms) if uncategorized_platforms else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to split personas: {str(e)}")
