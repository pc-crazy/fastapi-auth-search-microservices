import os
from typing import Optional
from sqlalchemy import or_

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session, joinedload
from urllib.parse import urlencode

from .models import Location, Company, Department, Position
from .db import get_db
from .models import Employee
from .org_config import get_org_columns
from .ratelimit import is_allowed

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

app = FastAPI()


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload["user_id"], "org_id": payload["org_id"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


def status_label(code: int) -> str:
    return {
        1: "active",
        2: "not started",
        3: "terminated"
    }.get(code, "unknown")


@app.get("/search")
def search_employees(
        q: Optional[str] = "",
        status: Optional[int] = Query(None, ge=1, le=3),
        location: Optional[str] = None,
        company: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None,
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        request: Request = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    ip = request.client.host
    if not is_allowed(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    org_id = current_user["org_id"]
    columns = get_org_columns(org_id)

    # Base query
    query = db.query(Employee)
    options = []
    joins_needed = set()

    # Dynamically collect joins required
    if any(col in columns for col in ["location"]) or location or (q and "location" in columns):
        joins_needed.add("location")
        options.append(joinedload(Employee.location))

    if any(col in columns for col in ["company"]) or company or (q and "company" in columns):
        joins_needed.add("company")
        options.append(joinedload(Employee.company))

    if any(col in columns for col in ["department"]) or department or (q and "department" in columns):
        joins_needed.add("department")
        options.append(joinedload(Employee.department))

    if any(col in columns for col in ["position"]) or position or (q and "position" in columns):
        joins_needed.add("position")
        options.append(joinedload(Employee.position))

    query = query.options(*options).filter(Employee.org_id == org_id)

    # Apply joins only if needed
    if "location" in joins_needed:
        query = query.join(Employee.location)
    if "company" in joins_needed:
        query = query.join(Employee.company)
    if "department" in joins_needed:
        query = query.join(Employee.department)
    if "position" in joins_needed:
        query = query.join(Employee.position)

    # Apply filters
    if status:
        query = query.filter(Employee.status == status)
    if location:
        query = query.filter(Location.name.ilike(f"%{location}%"))
    if company:
        query = query.filter(Company.name.ilike(f"%{company}%"))
    if department:
        query = query.filter(Department.name.ilike(f"%{department}%"))
    if position:
        query = query.filter(Position.name.ilike(f"%{position}%"))

    # Apply full-text q search only on visible fields
    if q:
        q_clauses = []
        if "first_name" in columns:
            q_clauses.append(Employee.first_name.ilike(f"%{q}%"))
        if "last_name" in columns:
            q_clauses.append(Employee.last_name.ilike(f"%{q}%"))
        if "department" in columns:
            q_clauses.append(Department.name.ilike(f"%{q}%"))
        if "company" in columns:
            q_clauses.append(Company.name.ilike(f"%{q}%"))
        if "position" in columns:
            q_clauses.append(Position.name.ilike(f"%{q}%"))
        if "location" in columns:
            q_clauses.append(Location.name.ilike(f"%{q}%"))

        if q_clauses:
            query = query.filter(or_(*q_clauses))

    total = query.count()
    employees = query.offset(offset).limit(limit).all()

    results = []
    for emp in employees:
        row = {}
        for col in columns:
            if col == "status":
                row[col] = status_label(emp.status)
            elif col == "location":
                row[col] = emp.location.name
            elif col == "company":
                row[col] = emp.company.name
            elif col == "department":
                row[col] = emp.department.name
            elif col == "position":
                row[col] = emp.position.name
            elif col == "first_name":
                row[col] = emp.first_name
            elif col == "last_name":
                row[col] = emp.last_name
            else:
                row[col] = getattr(emp, col, None)
        results.append(row)

    # Pagination
    base_url = str(request.url).split('?')[0]
    query_params = dict(request.query_params)

    def build_url(new_offset):
        query_params["offset"] = str(new_offset)
        return f"{base_url}?{urlencode(query_params)}"

    next_url = build_url(offset + limit) if offset + limit < total else None
    prev_url = build_url(max(offset - limit, 0)) if offset > 0 else None

    return {
        "total": total,
        "count": len(results),
        "next": next_url,
        "previous": prev_url,
        "results": results
    }
