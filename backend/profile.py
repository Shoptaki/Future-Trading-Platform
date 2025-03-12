from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, User
from pydantic import BaseModel
from backend.auth import verify_token

router = APIRouter(tags=["Profile"])

# Pydantic model for profile update request
class UserProfileUpdate(BaseModel):
    email: str
    first_name: str
    last_name: str

# ✅ Get User Profile
@router.get("/profile")
def get_profile(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

# ✅ Update User Profile
@router.put("/profile")
def update_profile(
    profile_data: UserProfileUpdate,
    username: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = profile_data.email
    user.first_name = profile_data.first_name
    user.last_name = profile_data.last_name

    db.commit()
    db.refresh(user)

    return {"message": "Profile updated successfully"}
