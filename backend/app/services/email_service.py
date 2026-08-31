import os
import json
from datetime import datetime

EMAIL_DIR = os.path.join(os.getcwd(), 'email_logs')
if not os.path.exists(EMAIL_DIR):
    os.makedirs(EMAIL_DIR, exist_ok=True)


def send_email(to: str, subject: str, body: str, meta: dict = None):
    """Demo email logger: writes the email contents to a file in email_logs/ for inspection.
    This does NOT send real emails. Use this for demo/audit of alerts.
    Returns the filename written.
    """
    meta = meta or {}
    timestamp = datetime.utcnow().isoformat()
    payload = {
        'to': to,
        'subject': subject,
        'body': body,
        'meta': meta,
        'timestamp': timestamp
    }
    safe_ts = timestamp.replace(':','').replace('-','').replace('.','')
    filename = f"email_{safe_ts}_{abs(hash(to)) % 10000}.json"
    path = os.path.join(EMAIL_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return filename


def list_emails(limit: int = 100):
    files = sorted(os.listdir(EMAIL_DIR), reverse=True)[:limit]
    return files


def read_email(filename: str):
    path = os.path.join(EMAIL_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
