"""OAuth helper endpoints for GitHub linking.

This module exposes two endpoints:
- GET /auth/github/login?state=<token>  -> redirects to GitHub OAuth authorize
- GET /auth/github/callback?code=...&state=... -> exchanges code and saves mapping

Behavior:
- The frontend should include the current Clerk JWT in `state` when redirecting the user to
  `/auth/github/login?state=<CLERK_JWT>` so the callback can associate the GitHub account with the
  Clerk user. `state` is optional but recommended.
"""

import os
import jwt
from fastapi import FastAPI, Request, HTTPException
import httpx
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

app = FastAPI()

# GitHub app credentials (must be set in environment)
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI', 'https://your.app/github/callback')

# Database setup (reuse same env vars as main app)
DB_USER = os.getenv('POSTGRES_USER', 'chimera_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'chimera_password')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'chimera_db')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/auth/github/login")
def github_login(state: str = None):
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "read:user user:email",
        "allow_signup": "false"
    }
    if state:
        params["state"] = state

    url = "https://github.com/login/oauth/authorize"
    return RedirectResponse(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()))


@app.get("/auth/github/callback")
async def github_callback(code: str, request: Request, state: str = None):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI
            }
        )
        token_resp.raise_for_status()
        token_json = token_resp.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise HTTPException(400, "No access token")

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}", "Accept": "application/json"}
        )
        user_resp.raise_for_status()
        user = user_resp.json()

    # If state was provided, try to decode clerk_id from it and save mapping in DB
    clerk_id = None
    if state:
        try:
            # Attempt to decode Clerk JWT without verifying signature (consistent with auth.get_clerk_user_id)
            payload = jwt.decode(state, options={"verify_signature": False})
            clerk_id = payload.get("sub")
        except Exception:
            clerk_id = None

    if clerk_id:
        db = SessionLocal()
        try:
            user_obj = db.query(User).filter_by(clerk_id=clerk_id).first()
            if not user_obj:
                # Create user if not exist
                user_obj = User(clerk_id=clerk_id, email=None)
                db.add(user_obj)
                db.commit()
                db.refresh(user_obj)

            # Persist GitHub info
            user_obj.github_handle = user.get("login")
            user_obj.github_id = str(user.get("id")) if user.get("id") else None
            db.add(user_obj)
            db.commit()
        finally:
            db.close()

    return {"verified_handle": user["login"], "github_id": user["id"], "clerk_id": clerk_id}