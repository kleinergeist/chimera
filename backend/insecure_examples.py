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
# CWE-434: Unrestricted File Upload with Dangerous Type
# ============================================================================

def insecure_file_upload_zip(uploaded_file) -> str:
    """
    ✗ VULNERABLE: Allows uploading ZIP files which can be extracted
    Aikido should flag: No file type validation on uploads
    """
    # No validation of archive contents
    import zipfile
    extracted_path = f"/tmp/uploads/{uploaded_file.filename}"
    with zipfile.ZipFile(uploaded_file.file, 'r') as zip_ref:
        zip_ref.extractall(extracted_path)  # ✗ Zip slip vulnerability
    return extracted_path


# ============================================================================
# CWE-540: Exposure of Private Information
# ============================================================================

def insecure_debug_endpoint(user_id: int) -> dict:
    """
    ✗ VULNERABLE: Debug endpoint exposes internal system information
    Aikido should flag: Sensitive data in debug response
    """
    import sys
    import platform
    
    return {
        "debug_info": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "environment_vars": dict(os.environ),  # ✗ Exposes all env vars
            "user_id": user_id,
            "database_host": os.getenv("DB_HOST"),
            "api_keys": os.getenv("API_KEY"),
        }
    }


# ============================================================================
# CWE-611: Server-Side Request Forgery (SSRF) via Custom Headers
# ============================================================================

def insecure_proxy_request(url: str, headers: dict) -> str:
    """
    ✗ VULNERABLE: Allows proxying requests with custom headers
    Aikido should flag: User-controlled headers in requests
    """
    import requests
    
    # Attacker can inject Authorization headers, bypass IP restrictions
    response = requests.get(
        url,
        headers=headers,  # ✗ User controls all headers
        verify=False,  # ✗ No SSL verification
        allow_redirects=True  # ✗ Follows redirects without limit
    )
    return response.text


# ============================================================================
# CWE-326: Inadequate Encryption Strength (Hardcoded Cipher)
# ============================================================================

def insecure_aes_encryption(data: str) -> bytes:
    """
    ✗ VULNERABLE: Uses hardcoded, weak AES encryption
    Aikido should flag: Weak/hardcoded encryption key
    """
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    
    # Key is hardcoded and too short (128-bit = 16 bytes)
    key = b"hardcoded_key!!!"  # ✗ Hardcoded 16-byte key
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # ECB mode would be even worse
    return cipher.encrypt(data.ljust(16))  # ✗ No padding


# ============================================================================
# CWE-640: Weak Password Recovery Implementation
# ============================================================================

def insecure_password_recovery_token() -> str:
    """
    ✗ VULNERABLE: Password reset token can be predicted
    Aikido should flag: Weak random token generation
    """
    import random
    import string
    
    # Uses predictable random module
    token = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(6)  # ✗ Only 6 characters!
    )
    return token


# ============================================================================
# CWE-22 + CWE-36: Zip Slip Vulnerability (Advanced)
# ============================================================================

def insecure_extract_archive(archive_path: str, target_dir: str) -> None:
    """
    ✗ VULNERABLE: Zip slip allows extracting outside target directory
    Aikido should flag: Unsafe archive extraction
    
    Attack: Archive contains "../../../etc/passwd"
    """
    import tarfile
    import zipfile
    
    # No path validation during extraction
    if archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(target_dir)  # ✗ Zip slip possible
    elif archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extractall(target_dir)  # ✗ Zip slip possible


# ============================================================================
# CWE-639: Authorization Through User-Controlled Key
# ============================================================================

def insecure_permission_check(user_id: int, request_user_id: int) -> dict:
    """
    ✗ VULNERABLE: Authorization bypass via user-provided role
    Aikido should flag: Missing role verification
    """
    user_role = request_user_id  # ✗ Trust user-provided role
    
    if user_role > 5:  # Assume high role = admin
        return {
            "admin": True,
            "all_users": "complete_list",
            "api_keys": "all_keys"
        }
    return {"admin": False}


# ============================================================================
# CWE-476: Null Pointer Dereference with Type Confusion
# ============================================================================

def insecure_type_confusion(user_input: any) -> str:
    """
    ✗ VULNERABLE: No type checking before operations
    Aikido should flag: Unsafe type operations
    """
    # Attacker sends: null, array, object instead of string
    name = user_input["name"]  # ✗ KeyError if not dict
    age = user_input["age"]  # ✗ Could be any type
    
    # Type confusion
    result = f"User {name} is {age + 1} years old"  # ✗ TypeError if age is string
    return result


# ============================================================================
# CWE-95: Injection via Code Comments (Polyglot Attack)
# ============================================================================

def insecure_template_string(user_template: str) -> str:
    """
    ✗ VULNERABLE: Template string injection
    Aikido should flag: User input in template rendering
    """
    from jinja2 import Template
    
    # User controls entire template including comments
    template = Template(user_template)
    # Attack: "{{ ''.__class__.__mro__[1].__subclasses__() }}"
    return template.render()


# ============================================================================
# CWE-113: Improper Neutralization of CRLF in HTTP Headers
# ============================================================================

def insecure_http_response_splitting(header_value: str) -> dict:
    """
    ✗ VULNERABLE: HTTP response splitting via headers
    Aikido should flag: Unvalidated header values
    """
    # Attacker can inject CRLF (%0d%0a) to add fake headers
    response = {
        "Set-Cookie": f"sessionid={header_value}",  # ✗ No CRLF validation
        "Content-Type": "application/json"
    }
    return response


# ============================================================================
# CWE-352: Cross-Site Request Forgery (CSRF) Token Bypass
# ============================================================================

def insecure_csrf_validation(csrf_token: str, expected_token: str) -> bool:
    """
    ✗ VULNERABLE: Weak CSRF token validation
    Aikido should flag: Insufficient token checking
    """
    # Only checks if token is non-empty (!)
    if csrf_token and len(csrf_token) > 0:  # ✗ Insufficient validation
        return True
    
    # Or: Always returns True on GET requests
    return True  # ✗ No actual validation


# ============================================================================
# CWE-94: Improper Control of Generation of Code (Code Injection)
# ============================================================================

def insecure_string_interpolation(username: str) -> str:
    """
    ✗ VULNERABLE: Code generation via string interpolation
    Aikido should flag: Dynamic code generation
    """
    # This is basically a backdoor
    code = f"""
def check_user():
    if username == '{username}':  # ✗ Vulnerable to injection
        return True
    return False
"""
    # Then execute with exec/eval
    exec(code)  # ✗ Arbitrary code execution
    return "User check function created"


# ============================================================================
# CWE-807: Reliance on Untrusted Inputs in a Security Decision
# ============================================================================

def insecure_token_validation(token: str, user_agent: str) -> bool:
    """
    ✗ VULNERABLE: Security decision based on user input
    Aikido should flag: Trusting user-provided validation data
    """
    # Attacker controls both token and user_agent
    # Uses user_agent as "validation" (!)
    if user_agent == "Mozilla/5.0":  # ✗ Easily spoofed
        return True
    
    if token.startswith("Bearer "):  # ✗ Format check only, no signature
        return True
    
    return False


# ============================================================================
# CWE-326: Weak Key Generation
# ============================================================================

def insecure_weak_key_derivation(password: str) -> bytes:
    """
    ✗ VULNERABLE: Weak password hashing
    Aikido should flag: Insufficient key derivation
    """
    import hashlib
    
    # MD5 with no salt - extremely weak
    key = hashlib.md5(password.encode()).digest()  # ✗ MD5 is broken
    
    # Or: Single iteration of SHA256 (should be 100k+)
    key = hashlib.sha256(password.encode()).digest()  # ✗ No iterations
    
    return key


# ============================================================================
# CWE-1025: Comparison Using Wrong Factors
# ============================================================================

def insecure_version_check(current: str, minimum: str) -> bool:
    """
    ✗ VULNERABLE: String comparison for versions
    Aikido should flag: Wrong comparison logic
    
    "1.9" > "1.10" returns True (lexicographic)
    But numerically 1.9 < 1.10
    """
    if current > minimum:  # ✗ String comparison, not version
        return True
    return False


# ============================================================================
# CWE-200: Sensitive Data Exposure in Cache
# ============================================================================

def insecure_caching(user_id: int, sensitive_data: dict) -> dict:
    """
    ✗ VULNERABLE: Sensitive data stored in cache without TTL
    Aikido should flag: Sensitive data caching
    """
    import functools
    
    @functools.lru_cache(maxsize=1000)
    def get_user_profile(uid):
        return {
            "user_id": uid,
            "ssn": "123-45-6789",  # ✗ PII in cache
            "credit_card": "4111-1111-1111-1111",  # ✗ PII in cache
            "api_key": os.getenv("SECRET_KEY")  # ✗ Secrets in cache
        }
    
    return get_user_profile(user_id)


# ============================================================================
# CWE-776: Improper Restriction of Recursive Entity References (Billion Laughs)
# ============================================================================

def insecure_xml_entity_expansion(xml_input: str) -> dict:
    """
    ✗ VULNERABLE: XML Billion Laughs attack (DoS)
    Aikido should flag: Unrestricted XML entity expansion
    
    Attack: XML with recursive entity definitions consuming memory
    """
    import xml.etree.ElementTree as ET
    
    # Vulnerable to entity expansion attack
    try:
        root = ET.fromstring(xml_input)  # ✗ Billion laughs vulnerable
        return {"parsed": True}
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# CWE-639: Authorization Bypass via Object Reference
# ============================================================================

def insecure_object_access(object_id: int, user_id: int) -> dict:
    """
    ✗ VULNERABLE: No verification of object ownership
    Aikido should flag: Missing authorization check
    
    Attacker changes object_id to access other users' data
    """
    # Directly access object without checking ownership
    return {
        "object_id": object_id,
        "data": f"User {user_id}'s data for object {object_id}"
        # ✗ No check: Does user_id own object_id?
    }


# ============================================================================
# Test/Demo Function
# ============================================================================

if __name__ == "__main__":
    """
    This section demonstrates how Aikido should detect these vulnerabilities.
    """
    print("🔓 INSECURE EXAMPLES - For Security Testing Only")
    print("=" * 70)
    print("\n✗ CRITICAL Vulnerabilities (50+ Documented):")
    print("\n  CATEGORY: Remote Code Execution (RCE)")
    print("    1. Unsafe subprocess with shell=True (CWE-78)")
    print("    2. Unsafe eval() and exec() (CWE-95, CWE-506)")
    print("    3. Pickle deserialization (CWE-502)")
    print("    4. XML External Entity (XXE) injection (CWE-611)")
    print("    5. Jinja2/Template SSTI (CWE-1336)")
    print("    6. Dynamic code generation (CWE-94)")
    print("    7. String interpolation in code (CWE-94)")
    print("    8. Unsafe dynamic imports (CWE-99)")
    print("    9. File upload + code import (CWE-434+427)")
    print("   10. Zip slip extraction (CWE-22+36)")
    
    print("\n  CATEGORY: Injection Attacks")
    print("   11. SQL injection via f-string (CWE-89)")
    print("   12. SQL injection via .format() (CWE-89)")
    print("   13. OS command injection (CWE-78)")
    print("   14. HTTP response splitting (CWE-113)")
    print("   15. Template injection (CWE-1336)")
    
    print("\n  CATEGORY: Authentication & Cryptography")
    print("   16. JWT not verified (CWE-347)")
    print("   17. Weak password hashing (CWE-326)")
    print("   18. Weak key derivation (CWE-326)")
    print("   19. Weak random token generation (CWE-327)")
    print("   20. Weak password recovery (CWE-640)")
    print("   21. MD5/SHA1 for security (CWE-327)")
    
    print("\n  CATEGORY: Authorization & Access Control")
    print("   22. Authorization bypass via parameter (CWE-863)")
    print("   23. Missing resource ownership check (CWE-285)")
    print("   24. CSRF token bypass (CWE-352)")
    print("   25. Weak session token validation (CWE-639)")
    print("   26. User-controlled role (CWE-639)")
    print("   27. Untrusted input in security decision (CWE-807)")
    print("   28. Object reference without auth (CWE-639)")
    print("   29. Permission check via user input (CWE-639)")
    print("   30. Type confusion in authorization (CWE-476)")
    
    print("\n  CATEGORY: Data Exposure & Validation")
    print("   31. Plaintext password storage (CWE-256)")
    print("   32. Debug endpoint exposes secrets (CWE-540)")
    print("   33. Sensitive data in cache (CWE-200)")
    print("   34. Sensitive data in logs (CWE-200)")
    print("   35. Environment variables exposure (CWE-798)")
    print("   36. Hardcoded secrets in code (CWE-798)")
    print("   37. Null pointer/type confusion (CWE-476)")
    print("   38. Unvalidated header values (CWE-113)")
    print("   39. Wrong type comparison (CWE-1025)")
    print("   40. Path traversal (CWE-22)")
    
    print("\n  CATEGORY: Network & SSRF")
    print("   41. Disabled SSL verification (CWE-295)")
    print("   42. SSRF via proxy request (CWE-918)")
    print("   43. User-controlled URL headers (CWE-918)")
    print("   44. Unvalidated redirects (CWE-601)")
    print("   45. Open redirect (CWE-601)")
    
    print("\n  CATEGORY: File Operations & Upload")
    print("   46. Unrestricted file upload (CWE-434)")
    print("   47. Zip file upload (CWE-434)")
    print("   48. Archive extraction without validation (CWE-22+36)")
    print("   49. File read with path traversal (CWE-22)")
    print("   50. User-controlled file path (CWE-22)")
    
    print("\n  CATEGORY: DoS & Resource Exhaustion")
    print("   51. No rate limiting (CWE-770)")
    print("   52. XML entity expansion (CWE-776)")
    print("   53. Billion laughs attack (CWE-776)")
    
    print("\n  CATEGORY: Configuration Issues")
    print("   54. CORS misconfiguration (CWE-1021)")
    print("   55. Debug mode exposed (CWE-215)")
    print("   56. Hardcoded endpoints (CWE-665)")
    print("   57. CRLF in headers (CWE-113)")
    
    print("\n" + "=" * 70)
    print("Total: 57+ documented insecurities for Aikido scanning")
    print("⚠️  DO NOT USE THIS CODE IN PRODUCTION!")
    print("=" * 70)
