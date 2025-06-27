import re

SQLI_PATTERNS = [
    r"(?i)union.*select",
    r"(?i)or\s+\d+=\d+",
    r"(?i)or\s+'[^']*'='[^']*'",
    r"(?i)(\%27)|(')",
    r"(?i)select.+from",
    r"(?i)drop\s+table",
    r"(?i)insert\s+into",
    r"(?i)--|#|/\*",
    r"(?i)benchmark\s*\(\s*\d+,\s*.*\)",
    r"(?i)sleep\s*\(\s*\d+\s*\)",
    r"(?i)waitfor\s+delay"
]

def is_sqli(payload: str) -> bool:
    return any(re.search(pattern, payload) for pattern in SQLI_PATTERNS)
