import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
import jwt

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    DEMO LOGIN — REPLACE WITH PRODUCTION AUTH FOR SIH
    Default demo account: officer / officer123
    """
    user = db.query(User).filter(User.username == payload.username).first()
    
    # Auto-seed demo officer if missing
    if not user and payload.username == "officer" and payload.password == "officer123":
        hashed_pwd = get_password_hash("officer123")
        user = User(
            username="officer",
            email="officer@agrirakshak.gov.in",
            hashed_password=hashed_pwd,
            role="officer",
            full_name="Demo Agricultural Officer"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user or not verify_password(payload.password, user.hashed_password):
        if payload.username == "officer" and payload.password == "officer123":
            access_token = create_access_token(data={"sub": "officer", "role": "officer"})
            return {"access_token": access_token, "token_type": "bearer"}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
