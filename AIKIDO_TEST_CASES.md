# Aikido Security Test Cases - Quick Reference

## Running Aikido Scan

```bash
# Scan the entire project
aikido scan

# Scan with detailed output
aikido scan --format json > aikido-report.json

# View results in Aikido dashboard
# Visit: https://app.aikido.dev/
```

---

## Expected Findings (37 Vulnerabilities)

### Quick Test: Run Individual Functions

```python
# Test file: backend/insecure_examples.py

# To verify detection, import and call:
python -c "from insecure_examples import *; print('Loaded all functions')"
```

---

## Vulnerability Test Matrix

### CRITICAL (RCE) - 10 Vulnerabilities

| # | Function | CWE | Test Command | Expected Aikido Flag |
|---|----------|-----|--------------|----------------------|
| 1 | `insecure_subprocess_shell()` | 78 | `insecure_subprocess_shell("; rm -rf /")` | ✅ Shell injection |
| 2 | `insecure_sql_query()` | 89 | `insecure_sql_query("' OR '1'='1")` | ✅ SQL injection |
| 3 | `insecure_pickle_load()` | 502 | `insecure_pickle_load(b'\x80\x04...')` | ✅ Pickle RCE |
| 4 | `insecure_reflection()` | 95 | `insecure_reflection({"code": "__import__('os').system('ls')"})` | ✅ Eval RCE |
| 5 | `insecure_xml_parse()` | 611 | `insecure_xml_parse("<!DOCTYPE ...XXE attack...")` | ✅ XXE injection |
| 6 | `insecure_dynamic_import()` | 99 | `insecure_dynamic_import("os")` | ⚠️ Dynamic import |
| 7 | `insecure_format_string()` | 95 | `insecure_format_string("{0.__class__.__bases__[0]}")` | ⚠️ Format string |
| 8 | `insecure_template_injection()` | 1336 | `insecure_template_injection("{{7*7}}")` | ⚠️ SSTI |
| 9 | `insecure_code_eval_endpoint()` | 506 | `insecure_code_eval_endpoint("os.system('id')")` | ✅ Eval backdoor |
| 10 | `insecure_exec_endpoint()` | 506 | `insecure_exec_endpoint("import os; os.system('whoami')")` | ✅ Exec backdoor |

---

### HIGH (Auth/Authz) - 7 Vulnerabilities

| # | Function | CWE | Test Scenario | Expected Aikido Flag |
|---|----------|-----|---------------|----------------------|
| 1 | JWT decode in `auth.py` | 347 | Decode JWT without signature | ✅ JWT verification disabled |
| 2 | `insecure_authorization_bypass()` | 863 | Call with `admin_flag=True` | ⚠️ Logic bypass |
| 3 | `insecure_resource_access()` | 285 | Access other user's data | ⚠️ Missing auth check |
| 4 | `insecure_https_request()` | 295 | `insecure_https_request("https://api.example.com")` | ✅ Disabled SSL verify |
| 5 | `insecure_file_upload()` | 434 | Upload `shell.php` | ✅ Unrestricted upload |
| 6 | `insecure_redirect()` | 601 | `insecure_redirect("https://evil.com")` | ⚠️ Open redirect |
| 7 | `insecure_session_token()` | 639 | Any 32 alphanumeric string | ⚠️ Weak validation |

---

### MEDIUM (Info Disclosure) - 11 Vulnerabilities

| # | Function | CWE | Test Case | Expected Aikido Flag |
|---|----------|-----|-----------|----------------------|
| 1 | `store_password_plaintext()` | 256 | Store password without hashing | ✅ Plaintext storage |
| 2 | `insecure_file_read()` | 22 | `insecure_file_read("../../etc/passwd")` | ✅ Path traversal |
| 3 | `insecure_weak_encryption_key()` | 326 | Use 5-byte key for Fernet | ⚠️ Weak key |
| 4 | `insecure_log_injection()` | 117 | `insecure_log_injection("login\nAdmin login")` | ⚠️ Log injection |
| 5 | `insecure_null_dereference()` | 476 | Call with missing dict keys | ⚠️ KeyError possible |
| 6 | `insecure_password_reset()` | 640 | Generate tokens from time | ✅ Weak random |
| 7 | `insecure_weak_random()` | 327 | Generate security token | ✅ Weak RNG |
| 8 | `insecure_error_handler()` | 200 | Catch exception, return str(e) | ⚠️ Info leak |
| 9 | `insecure_logging()` | 200 | Log username and password | ✅ Sensitive data in logs |
| 10 | `insecure_path_traversal_normalization()` | 1234 | Bypass with `..\\..\\` | ⚠️ Path bypass |
| 11 | `insecure_version_comparison()` | 1025 | Compare "1.9" vs "1.10" as strings | ⚠️ Wrong comparison |

---

### LOW (Config Issues) - 9 Vulnerabilities

| # | Function/File | CWE | Test Case | Expected Aikido Flag |
|---|--------|-----|-----------|----------------------|
| 1 | `insecure_cors_config()` | 1021 | Check CORS headers returned | ✅ Allow all origins |
| 2 | `insecure_no_rate_limit()` | 770 | Spam endpoint 1000x | ✅ No rate limiting |
| 3 | Global constants | 798 | Search for hardcoded keys | ✅ Hardcoded secrets |
| 4 | `insecure_hardcoded_api_endpoint()` | 665 | Check endpoint URL in code | ⚠️ Hardcoded endpoint |
| 5 | `insecure_secret_management()` | 798 | Print env var to stdout | ✅ Env exposure |
| 6 | `insecure_control_flow()` | 691 | Pass is_admin=True | ⚠️ Control flow flaw |
| 7 | `Dockerfile` | N/A | Check USER directive | ✅ Runs as root |
| 8 | `gosearch/Dockerfile` | 1104 | Check Go version date | ✅ Outdated Go |
| 9 | `gosearch/main.go` | 78 | Check os.Exec() call | ⚠️ Command injection |

---

## Aikido Detection Confidence

### ✅ High Confidence (Will Definitely Detect)
- SQL injection (CWE-89)
- Pickle deserialization (CWE-502)
- Shell injection subprocess (CWE-78)
- Eval/exec with user input (CWE-95, CWE-506)
- Hardcoded secrets (CWE-798)
- Weak random (CWE-327)
- Plaintext password logging (CWE-200)
- Disabled SSL verify (CWE-295)
- Unrestricted file upload (CWE-434)
- CORS misconfiguration (CWE-1021)
- Missing rate limiting (CWE-770)
- Docker root user (Docker security)

### ⚠️ Medium Confidence (Might Detect - Context Dependent)
- Authorization bypass (CWE-863, CWE-285) - requires flow analysis
- Log injection (CWE-117)
- NULL dereference (CWE-476)
- Path traversal (CWE-22, CWE-1234)
- Open redirect (CWE-601)
- Weak session tokens (CWE-639)
- Format string (CWE-95)
- SSTI (CWE-1336)

### 🔶 Low Confidence (Unlikely to Detect - Requires Deep Analysis)
- Control flow flaws (CWE-691)
- Version comparison logic (CWE-1025)
- Dynamic imports (CWE-99)
- Command injection in Go (depends on pattern)

---

## Continuous Testing

### 1. After Code Changes
```bash
# Scan after each modification
cd /path/to/chimera
aikido scan

# Export results
aikido scan --format json > aikido-$(date +%s).json
```

### 2. Pre-Commit Hook
```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
aikido scan --format json && echo "✅ Security scan passed"
```

### 3. CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Aikido Security Scan
  run: aikido scan --format json --fail-on-critical
```

---

## Remediation Checklist

### Phase 1: Critical Fixes (Today)
- [ ] Remove eval/exec endpoints
- [ ] Fix subprocess shell=True usage
- [ ] Remove pickle.loads()
- [ ] Fix SQL injection vulnerabilities
- [ ] Disable insecure_examples.py in production

### Phase 2: High Priority (This Week)
- [ ] Enable JWT signature verification
- [ ] Fix SSL certificate verification
- [ ] Implement proper authorization checks
- [ ] Move secrets to environment variables
- [ ] Add input validation middleware

### Phase 3: Medium Priority (This Sprint)
- [ ] Hash passwords with bcrypt
- [ ] Fix CORS configuration
- [ ] Implement file upload validation
- [ ] Add rate limiting
- [ ] Update Go version

### Phase 4: Verification
- [ ] Re-run Aikido scan
- [ ] Verify vulnerability count decreased
- [ ] Test with OWASP ZAP
- [ ] Perform manual security review
- [ ] Document all fixes in SECURITY.md

---

## Key Metrics

**Current State (Pre-Fix):**
- Total Vulnerabilities: 37
- Aikido Detected: ~20 (54%)
- Critical: 10
- High: 7
- Medium: 11
- Low: 9

**Target State (Post-Fix):**
- Total Vulnerabilities: 0 (insecure_examples.py removed)
- Aikido Detected: 0
- False Positives: <2%

---

## Additional Resources

### Aikido Documentation
- Official Docs: https://www.aikido.dev/docs
- API Reference: https://www.aikido.dev/api
- Community: https://github.com/AikidoSec

### Security Best Practices
- OWASP Top 10: https://owasp.org/Top10/
- CWE/SANS Top 25: https://cwe.mitre.org/top25/
- NIST Cybersecurity Framework: https://csrc.nist.gov/projects/cybersecurity-framework
- Python Security: https://python.readthedocs.io/en/stable/library/security_warnings.html

### Testing Tools
- OWASP ZAP: https://www.zaproxy.org/
- Bandit (Python): https://bandit.readthedocs.io/
- Semgrep: https://semgrep.dev/
- Snyk: https://snyk.io/

---

**Last Updated:** October 26, 2025  
**For:** Hackathon Security Challenge  
⚠️ **DO NOT USE THESE FUNCTIONS IN PRODUCTION**
