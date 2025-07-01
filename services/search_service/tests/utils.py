import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_test_token(user_id=1, org_id=1):
    payload = {
        "user_id": user_id,
        "org_id": org_id,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_expired_token(user_id=1, org_id=1):
    payload = {
        "user_id": user_id,
        "org_id": org_id,
        "exp": datetime.utcnow() - timedelta(minutes=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_invalid_token():
    return jwt.encode({"user_id": 1, "org_id": 1}, "invalidsecret", algorithm=ALGORITHM)
