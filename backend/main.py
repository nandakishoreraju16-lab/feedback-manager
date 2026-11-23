from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import functions

app = FastAPI()

# Lets the React app (Vite runs it on port 5173) call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models: they check the request body before our code runs.
# Wrong type or a rule broken (like empty username) -> FastAPI sends 422 by itself.

class RegisterIn(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginIn(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class FeedbackIn(BaseModel):
    subject: str = Field(min_length=1)
    message: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)


# A1 - Register
@app.post("/register")
def register_user(user: RegisterIn):
    if user.username.strip() == "" or user.password.strip() == "":
        raise HTTPException(status_code=422, detail="Username and password cannot be empty")
    if "@" not in user.email or "." not in user.email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Invalid email format")
    result = functions.register_user(username=user.username, email=user.email, password=user.password)
    if not result:
        raise HTTPException(status_code=409, detail="Email already registered")
    return {"message": "User registered successfully"}


# A2 - Login
@app.post("/login")
def login(data: LoginIn):
    token = functions.verify_login(email=data.email, password=data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return token


# A3 - Refresh
@app.post("/refresh")
def refresh(refresh_token = Header(None)):
    user_id = functions.verify_token(token=refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return {"access_token": functions.create_token(user_id=user_id, token_type="access")}


# E1 - Get my feedback
@app.get("/feedback")
def get_feedback(token = Header(None)):
    user_id = functions.verify_token(token=token, token_type="access")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_feedback(user_id=user_id)


# E2 - Submit feedback
@app.post("/feedback", status_code=201)
def add_feedback(data: FeedbackIn, token = Header(None)):
    user_id = functions.verify_token(token=token, token_type="access")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if data.subject.strip() == "" or data.message.strip() == "":
        raise HTTPException(status_code=422, detail="Subject and message cannot be empty")
    return functions.add_feedback(user_id=user_id, subject=data.subject, message=data.message, rating=data.rating)
