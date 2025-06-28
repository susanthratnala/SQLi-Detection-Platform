# Basic SQLi WAF Layer for Flask (Linux-Ready)

import re
from flask import request, abort

def detect_sql_injection():
    patterns = [
        r"(?i)(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(?i)(\bOR\b|\bAND\b).*(=)",
        r"(?i)UNION(\s)+SELECT",
        r"(?i)DROP(\s)+TABLE",
        r"(?i)xp_cmdshell",
        r"(?i)sleep\((\d+)\)"
    ]

    for field, value in request.form.items():
        for pattern in patterns:
            if re.search(pattern, value):
                print(f"[WAF] Blocked input: {value}")
                abort(403)
