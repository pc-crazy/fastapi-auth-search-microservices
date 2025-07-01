from services.auth_service.models import Base, User
from services.auth_service.db import engine, SessionLocal

Base.metadata.create_all(bind=engine)

db = SessionLocal()
db.add_all([
    User(name="user1", password="pass1", org_id=1),
    User(name="user2", password="pass2", org_id=2)
])
db.commit()
