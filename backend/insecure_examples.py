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
# CWE-863: Incorrect Authorization
# ============================================================================

def insecure_authorization_bypass(user_id: int, admin_flag: bool = False) -> dict:
    """
    ✗ VULNERABLE: Authorization check bypassed via parameter.
    Aikido should flag: Logic flaw in permission checks
    
    Attacker can pass admin_flag=True via query parameter.
    """
    # Trust user-provided admin_flag directly without verification
    if admin_flag:  # ✗ Trusts user input for authorization
        return {
            "admin": True,
            "sensitive_data": "all user records",
            "database_password": "prod_db_pass_123"
        }
    return {"admin": False, "data": "limited"}


# ============================================================================
# CWE-285: Improper Access Control
# ============================================================================

def insecure_resource_access(user_id: int, target_user_id: int) -> dict:
    """
    ✗ VULNERABLE: No verification that user can access target resource.
    Aikido should flag: Missing resource ownership check
    
    Attacker can access any user's data by changing target_user_id.
    """
    # Directly fetch and return without checking ownership
    db_query = f"SELECT * FROM user_profiles WHERE id = {target_user_id}"  # ✗ No permission check
    return {"user_profile": "sensitive_data"}


# ============================================================================
# CWE-295: Improper Certificate Validation
# ============================================================================

def insecure_https_request(url: str) -> str:
    """
    ✗ VULNERABLE: SSL certificate validation disabled.
    Aikido should flag: verify=False in requests/httpx
    
    Vulnerable to Man-in-the-Middle (MITM) attacks.
    """
    import requests
    response = requests.get(url, verify=False)  # ✗ No SSL verification!
    return response.text


def insecure_httpx_request(url: str) -> str:
    """
    ✗ VULNERABLE: HTTPS verification disabled with httpx.
    Aikido should flag: verify=False in async HTTP client
    """
    import httpx
    client = httpx.Client(verify=False)  # ✗ Disabled certificate verification
    response = client.get(url)
    return response.text


# ============================================================================
# CWE-434: Unrestricted Upload of File with Dangerous Type
# ============================================================================

def insecure_file_upload(uploaded_file) -> str:
    """
    ✗ VULNERABLE: No validation of uploaded file type.
    Aikido should flag: File upload without MIME type check
    
    Attacker can upload shell.php with image MIME type.
    """
    # No file type validation
    filename = uploaded_file.filename
    filepath = f"/uploads/{filename}"  # ✗ No sanitization
    
    # Save directly without validation
    with open(filepath, "wb") as f:
        f.write(uploaded_file.file.read())  # ✗ Arbitrary file upload
    
    return filepath


# ============================================================================
# CWE-476: NULL Pointer Dereference
# ============================================================================

def insecure_null_dereference(user_data: dict) -> str:
    """
    ✗ VULNERABLE: No null/None checks before accessing dict keys.
    Aikido should flag: Unsafe dict access without validation
    """
    # Assumes keys exist without checking
    username = user_data["username"]  # ✗ KeyError if not present
    email = user_data["email"]  # ✗ KeyError if not present
    return f"{username}: {email}"


# ============================================================================
# CWE-117: Log Injection
# ============================================================================

def insecure_log_injection(user_input: str) -> None:
    """
    ✗ VULNERABLE: User input directly in log messages.
    Aikido should flag: Unsanitized input in logging
    
    Attacker can inject log forging: "User login\nAdmin login successful"
    """
    import logging
    logger = logging.getLogger()
    # User input directly interpolated into log
    logger.info(f"User action: {user_input}")  # ✗ Log injection possible
    return None


# ============================================================================
# CWE-639: Authorization Bypass Through User-Controlled Key
# ============================================================================

def insecure_session_token(user_id: int, session_token: str) -> bool:
    """
    ✗ VULNERABLE: Session token validated based on format alone.
    Aikido should flag: Weak token validation
    """
    # Only checks if token looks valid, doesn't verify authenticity
    if len(session_token) == 32 and session_token.isalnum():  # ✗ Insufficient validation
        return True
    return False


# ============================================================================
# CWE-601: URL Redirection to Untrusted Site (Open Redirect)
# ============================================================================

def insecure_redirect(redirect_url: str) -> dict:
    """
    ✗ VULNERABLE: Unvalidated URL redirect.
    Aikido should flag: Redirect without URL validation
    
    Attacker can redirect to: http://evil.com/steal_password
    """
    # No validation of redirect URL
    return {
        "redirect": redirect_url,  # ✗ Open redirect vulnerability
        "status": 302
    }


# ============================================================================
# CWE-326: Inadequate Encryption Strength
# ============================================================================

def insecure_weak_encryption_key() -> bytes:
    """
    ✗ VULNERABLE: Encryption key too short (only 8 bytes).
    Aikido should flag: Weak key size for encryption
    """
    # Only 8 bytes = 64 bits, far too weak
    weak_key = b"short"  # ✗ Only 5 bytes!
    
    from cryptography.fernet import Fernet
    # Will fail or use insecure key expansion
    try:
        cipher = Fernet(weak_key)
    except Exception:
        pass
    
    return weak_key


# ============================================================================
# CWE-640: Weak Password Recovery Mechanism for Forgotten Password
# ============================================================================

def insecure_password_reset(username: str) -> str:
    """
    ✗ VULNERABLE: Password reset token is predictable/weak.
    Aikido should flag: Weak token generation
    """
    import time
    # Token is just timestamp - easily guessable
    reset_token = str(int(time.time()))  # ✗ Sequential/predictable token
    
    # Send to user email (but token is weak)
    print(f"Reset token for {username}: {reset_token}")
    return reset_token


# ============================================================================
# CWE-1234: Improper Normalization of Elements in Control Flow
# ============================================================================

def insecure_path_traversal_normalization(user_path: str) -> str:
    """
    ✗ VULNERABLE: Path normalization bypass.
    Aikido should flag: Insufficient path validation
    
    Attack: user_path = "..\\..\\windows\\system32\\config\\sam"
    """
    base_dir = "/app/uploads/"
    # Insufficient check - doesn't prevent traversal
    if not user_path.startswith(".."):  # ✗ Easily bypassed
        file_path = base_dir + user_path
        with open(file_path, "r") as f:
            return f.read()
    return ""


# ============================================================================
# CWE-1025: Comparison Using Wrong Factors
# ============================================================================

def insecure_version_comparison(version_string: str) -> bool:
    """
    ✗ VULNERABLE: String comparison instead of version comparison.
    Aikido should flag: Incorrect comparison logic
    
    "1.9" > "1.10" as strings (lexicographic), but should be False numerically.
    """
    min_version = "1.10"
    # String comparison, not version comparison
    if version_string > min_version:  # ✗ Wrong comparison type
        return True
    return False


# ============================================================================
# CWE-665: Improper Initialization with Hard-Coded Network Resource
# ============================================================================

def insecure_hardcoded_api_endpoint() -> str:
    """
    ✗ VULNERABLE: Hardcoded API endpoint instead of config.
    Aikido should flag: Hardcoded network resources
    """
    # Hardcoded production endpoint - inflexible
    api_endpoint = "https://api.production.com/v1/users"  # ✗ Hardcoded
    return api_endpoint


# ============================================================================
# CWE-691: Insufficient Control Flow Management
# ============================================================================

def insecure_control_flow(user_id: int, is_admin: bool) -> dict:
    """
    ✗ VULNERABLE: Control flow doesn't properly enforce restrictions.
    Aikido should flag: Logic flaw in access control
    """
    user_data = {
        "id": user_id,
        "role": "user",
        "is_admin": is_admin  # ✗ Trusts user-provided admin flag
    }
    
    # Grants access based on untrusted input
    if user_data["is_admin"]:
        return {
            "admin_panel": True,
            "all_users": "sensitive_data",
            "system_config": "secrets"
        }
    
    return {"user_panel": True}


# ============================================================================
# CWE-99: Improper Control of Dynamically-Managed Code Resources
# ============================================================================

def insecure_dynamic_import(module_name: str):
    """
    ✗ VULNERABLE: Dynamic import of user-controlled module.
    Aikido should flag: __import__() with user input
    
    Attacker can import: "os", "subprocess", "shutil" etc.
    """
    # User can specify any module to import
    module = __import__(module_name)  # ✗ Arbitrary module import
    return module


# ============================================================================
# CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code
# ============================================================================

def insecure_format_string(user_input: str) -> str:
    """
    ✗ VULNERABLE: Format string vulnerability.
    Aikido should flag: format() with untrusted input
    """
    template = "{0.__class__.__bases__[0].__subclasses__()}"
    # User controls format string - can leak memory
    result = template.format(user_input)  # ✗ Format string attack
    return result


# ============================================================================
# CWE-611: Server-Side Template Injection
# ============================================================================

def insecure_template_injection(user_template: str) -> str:
    """
    ✗ VULNERABLE: Template rendering with user input.
    Aikido should flag: Unescaped template rendering
    """
    from jinja2 import Template
    
    # User controls template directly - allows SSTI
    template = Template(user_template)  # ✗ No sandbox/escaping
    result = template.render(context="data")
    return result


# ============================================================================
# CWE-798: Exposed API Keys in Code
# ============================================================================

STRIPE_API_KEY = "sk_live_stripe_key_12345"  # ✗ Hardcoded Stripe key
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnop"  # ✗ Hardcoded GitHub token
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"  # ✗ Hardcoded AWS secret
DATABASE_URL = "postgresql://user:pass123@prod-db.aws.com/maindb"  # ✗ Hardcoded DB URL


# ============================================================================
# CWE-506: Embedded Malicious Code
# ============================================================================

def insecure_code_eval_endpoint(code_string: str) -> any:
    """
    ✗ VULNERABLE: Evaluating arbitrary code from user input.
    Aikido should flag: eval() with user input (CRITICAL)
    
    This is essentially a backdoor.
    """
    # Direct code execution - complete compromise
    result = eval(code_string)  # ✗ CRITICAL: Arbitrary code execution
    return result


def insecure_exec_endpoint(code_string: str) -> None:
    """
    ✗ VULNERABLE: Executing arbitrary code statements.
    Aikido should flag: exec() with user input (CRITICAL)
    """
    # Execute any Python code - complete system compromise
    exec(code_string)  # ✗ CRITICAL: Arbitrary code execution


# ============================================================================
# CWE-434 + CWE-427: Code Injection via File Upload
# ============================================================================

def insecure_upload_and_import(uploaded_file) -> any:
    """
    ✗ VULNERABLE: Upload Python file and import it.
    Aikido should flag: File upload + dynamic import
    
    Attacker uploads malicious .py file which gets imported and executed.
    """
    import sys
    import importlib
    
    # Save uploaded file
    filepath = f"/tmp/{uploaded_file.filename}"
    with open(filepath, "wb") as f:
        f.write(uploaded_file.file.read())  # ✗ Unsafe upload
    
    # Add to path and import - executes code
    sys.path.insert(0, "/tmp")
    module_name = uploaded_file.filename.replace(".py", "")
    module = importlib.import_module(module_name)  # ✗ Executes uploaded code
    
    return module


# ============================================================================
# CWE-215: Information Exposure Through Debug Information
# ============================================================================

def insecure_debug_output(secret_data: str, public_flag: bool = True) -> None:
    """
    ✗ VULNERABLE: Debug information exposed in production.
    Aikido should flag: Sensitive data in print/debug statements
    """
    if public_flag:  # Might be True in production
        print(f"DEBUG: Processing secret: {secret_data}")  # ✗ Info leak
        print(f"DEBUG: API Key: {os.getenv('API_KEY')}")  # ✗ Env var leak


# ============================================================================
# Test/Demo Function
# ============================================================================

if __name__ == "__main__":
    """
    This section demonstrates how Aikido should detect these vulnerabilities.
    """
    
