from datetime import datetime, timedelta

RATE_LIMIT = 5
RATE_PERIOD = timedelta(minutes=1)
user_requests = {}

def is_allowed(ip: str) -> bool:
    now = datetime.utcnow()
    user_requests.setdefault(ip, []).append(now)
    user_requests[ip] = [t for t in user_requests[ip] if now - t < RATE_PERIOD]
    return len(user_requests[ip]) <= RATE_LIMIT
