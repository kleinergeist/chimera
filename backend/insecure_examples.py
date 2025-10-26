"""
insecure_examples.py

This module contains INTENTIONAL SECURITY VULNERABILITIES for testing Aikido
and other security scanning tools. 

⚠️ DO NOT USE THIS CODE IN PRODUCTION ⚠️

This is for hackathon security challenge testing only.
Each function demonstrates a common vulnerability that Aikido should detect.
"""

import os
import pickle
import json
import jwt
from datetime import datetime

# ============================================================================
# CWE-798: Hardcoded Secrets
# ============================================================================

HARDCODED_API_KEY = "sk_live_abcdef123456789"  # ✗ Hardcoded secret
HARDCODED_DB_PASSWORD = "admin_password_123"  # ✗ Hardcoded credential
HARDCODED_JWT_SECRET = "mysecretkey123"  # ✗ Hardcoded key


# ============================================================================
# CWE-347: Improper Verification of Cryptographic Signature
# ============================================================================

def insecure_jwt_decode(token: str) -> dict:
    """
    ✗ VULNERABLE: Decodes JWT without verifying signature.
    Aikido should flag: jwt.decode with verify_signature=False
    """
    payload = jwt.decode(
        token,
        options={"verify_signature": False}  # ✗ No signature check!
    )
    return payload


# ============================================================================
# CWE-256: Plaintext Storage of Password
# ============================================================================

def store_password_plaintext(username: str, password: str, db_connection) -> None:
    """
    ✗ VULNERABLE: Stores password in plaintext.
    Aikido should flag: sensitive data without encryption
    """
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    db_connection.execute(query)  # ✗ Also SQL injection vulnerable


def store_credit_card_plaintext(card_number: str, cvv: str) -> None:
    """
    ✗ VULNERABLE: Stores sensitive payment data plaintext.
    Aikido should flag: PII/credit card data in plaintext
    """
    with open("sensitive_data.txt", "w") as f:
        f.write(f"Card: {card_number}, CVV: {cvv}\n")  # ✗ Plaintext file


# ============================================================================
# CWE-89: SQL Injection
# ============================================================================

def insecure_sql_query(username: str, db_connection) -> dict:
    """
    ✗ VULNERABLE: SQL injection via string formatting.
    Aikido should flag: SQL query with string concatenation/f-string
    """
    # Attacker input: "admin' OR '1'='1"
    query = f"SELECT * FROM users WHERE username = '{username}'"  # ✗ SQL injection
    result = db_connection.execute(query)
    return result


def insecure_sql_with_format(email: str, db_connection) -> dict:
    """
    ✗ VULNERABLE: SQL injection using .format()
    Aikido should flag: String formatting in SQL
    """
    query = "SELECT * FROM users WHERE email = '{}'".format(email)  # ✗ SQL injection
    result = db_connection.execute(query)
    return result


# ============================================================================
# CWE-502: Deserialization of Untrusted Data
# ============================================================================

def insecure_pickle_load(user_data: bytes):
    """
    ✗ VULNERABLE: Deserializes untrusted pickle data.
    Aikido should flag: pickle.loads() on untrusted input
    Allows arbitrary code execution!
    """
    obj = pickle.loads(user_data)  # ✗ Arbitrary code execution vulnerability
    return obj


# ============================================================================
# CWE-78: OS Command Injection
# ============================================================================

def insecure_command_execution(username: str) -> str:
    """
    ✗ VULNERABLE: Command injection via os.system().
    Aikido should flag: os.system() with user input
    
    Attack: username = "test; rm -rf /"
    """
    result = os.system(f"gosearch -u {username}")  # ✗ Shell injection
    return result


def insecure_subprocess_shell(filename: str) -> str:
    """
    ✗ VULNERABLE: subprocess with shell=True.
    Aikido should flag: subprocess.run(..., shell=True)
    """
    import subprocess
    result = subprocess.run(f"ls {filename}", shell=True, capture_output=True)  # ✗ Shell injection
    return result.stdout.decode()


# ============================================================================
# CWE-306: Missing Authentication
# ============================================================================

def insecure_endpoint_no_auth(user_id: int) -> dict:
    """
    ✗ VULNERABLE: Endpoint with no authentication check.
    This would be called without verifying user is logged in.
    """
    # No authentication check - anyone can call this
    return {"user_id": user_id, "sensitive_data": "secret"}


# ============================================================================
# CWE-20: Improper Input Validation
# ============================================================================

def insecure_input_validation(user_input: str) -> None:
    """
    ✗ VULNERABLE: No input validation or sanitization.
    Aikido should flag: Use of unsanitized user input
    """
    # Attacker can pass:
    # - Very long strings (buffer overflow attempt)
    # - Special characters (path traversal)
    # - Script tags (XSS if used in web context)
    
    # Process directly without validation
    filename = f"/tmp/{user_input}"  # ✗ Path traversal possible
    with open(filename, "w") as f:
        f.write(user_input)


def insecure_reflection(user_data: dict) -> str:
    """
    ✗ VULNERABLE: Reflection/eval on user input.
    Aikido should flag: eval(), exec() with user data
    """
    # User sends: {"code": "__import__('os').system('rm -rf /')"}
    result = eval(user_data.get("code"))  # ✗ Arbitrary code execution
    return result


# ============================================================================
# CWE-327: Use of Broken Cryptography
# ============================================================================

def insecure_encryption(data: str) -> str:
    """
    ✗ VULNERABLE: Uses MD5 for encryption (cryptographically broken).
    Aikido should flag: MD5, DES, or other weak algorithms
    """
    import hashlib
    # MD5 is NOT encryption, it's a hash and is broken
    encrypted = hashlib.md5(data.encode()).hexdigest()  # ✗ Weak/broken crypto
    return encrypted


def insecure_weak_random(length: int = 10) -> str:
    """
    ✗ VULNERABLE: Uses weak random for security tokens.
    Aikido should flag: random module for cryptographic purposes
    """
    import random
    # random module is NOT cryptographically secure
    token = ''.join(random.choice('abcdefghijklmnop') for _ in range(length))  # ✗ Weak RNG
    return token


# ============================================================================
# CWE-22: Path Traversal
# ============================================================================

def insecure_file_read(filename: str) -> str:
    """
    ✗ VULNERABLE: Path traversal vulnerability.
    Aikido should flag: File operations with user-controlled paths
    
    Attack: filename = "../../etc/passwd"
    """
    # No path validation
    with open(filename, "r") as f:
        return f.read()


# ============================================================================
# CWE-611: Improper Restriction of XML External Entity Reference
# ============================================================================

def insecure_xml_parse(xml_data: str) -> dict:
    """
    ✗ VULNERABLE: XML External Entity (XXE) injection.
    Aikido should flag: XML parsing without disabling external entities
    """
    import xml.etree.ElementTree as ET
    # Vulnerable to XXE attacks
    root = ET.fromstring(xml_data)  # ✗ XXE vulnerable
    return root


# ============================================================================
# CWE-200: Exposure of Sensitive Information
# ============================================================================

def insecure_error_handler() -> dict:
    """
    ✗ VULNERABLE: Exposes sensitive information in error messages.
    Aikido should flag: Sensitive data in logs/exceptions
    """
    try:
        # Database operation
        pass
    except Exception as e:
        # Exposes full exception with DB credentials
        return {"error": str(e)}  # ✗ Sensitive info leak


def insecure_logging(username: str, password: str) -> None:
    """
    ✗ VULNERABLE: Logs sensitive credentials.
    Aikido should flag: Sensitive data in log statements
    """
    import logging
    logging.info(f"User {username} logged in with password {password}")  # ✗ Credentials in logs


# ============================================================================
# CWE-1021: CORS Misconfiguration
# ============================================================================

def insecure_cors_config() -> dict:
    """
    ✗ VULNERABLE: Overly permissive CORS configuration.
    Aikido should flag: Allow all origins or all methods
    """
    return {
        "Access-Control-Allow-Origin": "*",  # ✗ Allows any origin
        "Access-Control-Allow-Methods": "*",  # ✗ Allows all methods
        "Access-Control-Allow-Headers": "*",  # ✗ Allows all headers
        "Access-Control-Allow-Credentials": "true",  # ✗ Allows credentials with wildcard
    }


# ============================================================================
# CWE-770: Allocation of Resources Without Limits (DoS)
# ============================================================================

def insecure_no_rate_limit(user_input: str) -> list:
    """
    ✗ VULNERABLE: No rate limiting or request throttling.
    Aikido should flag: Missing rate limit decorators
    
    Attacker can spam this endpoint without limit.
    """
    # Process unlimited requests without throttling
    results = [process_item(item) for item in user_input.split(",")]  # ✗ No limits
    return results


def process_item(item: str) -> dict:
    return {"item": item, "processed": True}


# ============================================================================
# CWE-798: Secrets in Environment Variables (if not properly managed)
# ============================================================================

def insecure_secret_management() -> str:
    """
    ✗ VULNERABLE: If env vars are logged, printed, or exposed.
    Aikido should flag: Exposure of environment variables
    """
    secret = os.getenv("SECRET_KEY")
    print(f"Using secret key: {secret}")  # ✗ Exposed in logs/console
    return secret


# ============================================================================
# Test/Demo Function
# ============================================================================

if __name__ == "__main__":
    """
    This section demonstrates how Aikido should detect these vulnerabilities.
    """
    print("🔓 INSECURE EXAMPLES - For Security Testing Only")
    print("=" * 60)
    print("\n✗ Vulnerabilities that Aikido should detect:")
    print("  - Hardcoded secrets (CWE-798)")
    print("  - Disabled JWT verification (CWE-347)")
    print("  - Plaintext password storage (CWE-256)")
    print("  - SQL injection (CWE-89)")
    print("  - Command injection (CWE-78)")
    print("  - Insecure deserialization (CWE-502)")
    print("  - Missing authentication (CWE-306)")
    print("  - Weak input validation (CWE-20)")
    print("  - Weak cryptography (CWE-327)")
    print("  - Path traversal (CWE-22)")
    print("  - XXE injection (CWE-611)")
    print("  - Information exposure (CWE-200)")
    print("  - CORS misconfiguration (CWE-1021)")
    print("  - No rate limiting (CWE-770)")
    print("\n⚠️  DO NOT USE IN PRODUCTION!")
    print("=" * 60)
