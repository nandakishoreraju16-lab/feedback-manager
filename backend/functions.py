import os
from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# /app/data is mounted from /opt/feedback/data on EC2, so feedback.db survives redeploys
os.makedirs("/app/data", exist_ok=True)
DB_URL = "sqlite:////app/data/feedback.db"
engine = create_engine(DB_URL)
Base = declarative_base()

ACCESS_TOKEN_EXPIRY = 30 #mins
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60 #mins
SECRET_KEY = os.getenv("SECRET_KEY", "SECRET123")  # on EC2 it comes from the GitHub secret JWT_SECRET_KEY
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

# JWT login

def verify_login(email, password):
    session = Session(engine)
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        session.close()
        return False

    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        session.close()
        return False
    user_id = user.id
    session.close()
    access_token = create_token(user_id=user_id, token_type="access")
    refresh_token = create_token(user_id=user_id, token_type="refresh")
    return {"access_token": access_token, "refresh_token": refresh_token}


def create_token(user_id, token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "user_id": user_id,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return False
    if payload["token_type"] == token_type:
        return payload["user_id"]
    return False# hey there, database and login helpers coming up next
