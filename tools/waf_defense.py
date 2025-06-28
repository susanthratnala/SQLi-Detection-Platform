import re
import logging
from flask import request, abort, current_app

# Configure logging for WAF events
logging.basicConfig(
    filename='waf_logs.log',
    level=logging.WARNING,
    format='%(asctime)s [WAF] %(levelname)s: %(message)s'
)

# SQL Injection Detection Function
def detect_sql_injection():
    sqli_patterns = [
        r"(?i)(\%27)|(\')|(\-\-)|(\%23)|(#)",                    # Common SQL meta-characters
        r"(?i)\b(OR|AND)\b\s+[^\s]+(\s*=\s*[^\s]+)?",            # Boolean logic
        r"(?i)\bUNION\b\s+SELECT\b",                             # UNION SELECT
        r"(?i)\bDROP\b\s+TABLE\b",                               # DROP TABLE
        r"(?i)\bxp_cmdshell\b",                                  # MSSQL command exec
        r"(?i)\bsleep\s*\((\d+)\)",                              # Time-based blind SQLi
        r"(?i)\bWAITFOR\s+DELAY\b",                              # MS SQL delay
        r"(?i)\bSELECT\b.*\bFROM\b",                             # Generic SELECT FROM
        r"(?i)[\s\W](LIKE|IN)\s*\(",                             # LIKE/IN with list
        r"(?i)['\"]\s*=\s*['\"]"                                 # Tautologies like `'='`
    ]

    for field, value in request.form.items():
        for pattern in sqli_patterns:
            if re.search(pattern, value):
                msg = f"Potential SQLi attempt in field '{field}': {value}"
                logging.warning(msg)
                print(f"[WAF] Blocked malicious input: {value}")
                abort(403, description="SQL Injection attempt blocked.")

# Optional: Flask before_request hook
def register_sql_waf(app):
    @app.before_request
    def waf_wrapper():
        if request.method == "POST":
            detect_sql_injection()
