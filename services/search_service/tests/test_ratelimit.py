from freezegun import freeze_time
from datetime import timedelta, datetime
from services.search_service.ratelimit import is_allowed, user_requests, RATE_LIMIT, RATE_PERIOD

def test_rate_limit_allows_initial_requests():
    ip = "192.168.1.100"
    user_requests[ip] = []
    for _ in range(RATE_LIMIT):
        assert is_allowed(ip)

def test_rate_limit_blocks_after_threshold():
    ip = "192.168.1.101"
    user_requests[ip] = []
    for _ in range(RATE_LIMIT):
        is_allowed(ip)
    assert is_allowed(ip) is False

@freeze_time("2025-06-30 12:00:00")
def test_rate_limit_resets_after_period():
    ip = "192.168.1.102"
    user_requests[ip] = []

    now = datetime.utcnow()
    for _ in range(RATE_LIMIT):
        is_allowed(ip)

    assert is_allowed(ip) is False  # should be blocked now

    # Move time forward
    with freeze_time(now + RATE_PERIOD + timedelta(seconds=1)):
        assert is_allowed(ip) is True  # allowed after window resets

@freeze_time("2025-06-30 13:00:00")
def test_rate_limit_removes_old_entries():
    ip = "192.168.1.103"
    old_time = datetime.utcnow() - RATE_PERIOD - timedelta(seconds=10)
    user_requests[ip] = [old_time for _ in range(RATE_LIMIT)]

    assert is_allowed(ip) is True  # old requests are pruned
