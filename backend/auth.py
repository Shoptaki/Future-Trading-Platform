from fastapi import APIRouter, HTTPException, Depends, Form
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.database import SessionLocal, User
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt as pyjwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
import re

router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Secret key for JWT token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",bcrypt__rounds=12)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Password Policy Enforcement
def validate_password(password: str):
    """Validate password based on security policies."""
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")
    return True

# Pydantic Model for User Registration
class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

# User Registration Route
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    validate_password(user.password)  # Enforce password policy
    hashed_password = pwd_context.hash(user.password)  # ✅ Fixed variable name

    new_user = User(
        username=user.username,
        password_hash=hashed_password,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}

# User Login
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    print(f"🔹 Received Login Request → Username: {username}, Password: {password}")

    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        print("❌ User not found in database!")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not pwd_context.verify(password, user.password_hash):
        print(f"❌ Password does not match for user: {username}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print(f"✅ Login successful for {username}! Generating token...")

    access_token = create_access_token(
        {"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "user_id": user.id  # 🔹 Include user_id in the response
    }


# Token Verification
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username  # The username is extracted and can be used in protected routes.
    
    except pyjwt.ExpiredSignatureError:  # ✅ Fixed exception name
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except pyjwt.InvalidTokenError:  # ✅ Fixed exception name
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )



import re
from fastapi import HTTPException

def validate_password(password: str):
    """Validate password based on security policies."""
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")

    return True
