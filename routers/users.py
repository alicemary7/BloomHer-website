from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.users import User
from schemas.users import UserSignup, UserLogin
from dependencies import connect_db

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/signup")
def signup(data: UserSignup, db: Session = Depends(connect_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        password=data.password,  
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Signup successful"}


@user_router.post("/login")
def login(data: UserLogin, db: Session = Depends(connect_db)):

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password,
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }
