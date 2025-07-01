from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.auth_service.models import User
from services.auth_service.db import get_db

import os, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=req.username).first()
    if not user or user.password != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "user_id": user.id,
        "org_id": user.org_id,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
