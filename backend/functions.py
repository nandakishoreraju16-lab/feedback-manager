import os
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# feedback.db is kept inside the data folder so EC2 can keep it after redeploy
os.makedirs("data", exist_ok=True)
DB_PATH = "data/feedback.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

ACCESS_TOKEN_EXPIRY = 30 #mins
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60 #mins
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    message = Column(String)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)