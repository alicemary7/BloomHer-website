
from fastapi import APIRouter,Depends,HTTPException,status
from schemas.users import SignupSchema,LoginSchema
from models.users import UserLogin
from dependencies import connect_db
from sqlalchemy.orm import Session
from datetime import datetime

user_router=APIRouter(prefix="/users", tags=["Users_Details"])



# Signup

@user_router.post("/signup")
def signup(data: SignupSchema, db: Session = Depends(connect_db)):

    existing_user = db.query(UserLogin).filter(UserLogin.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")


    existing_email = db.query(UserLogin).filter(UserLogin.email == data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")


    new_user = UserLogin(
        username=data.username,
        email=data.email,
        password=data.password,
        phone=data.phone,
        created_at=data.created_at,
        updated_at=data.updated_at

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful!"}


# Login

@user_router.post("/login")
def login(data: LoginSchema, db: Session = Depends(connect_db)):

    user = db.query(UserLogin).filter(UserLogin.username == data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Login successful!"}


# Get_all_users

@user_router.get("/all_users")
def all_users(db:Session=Depends(connect_db)):
    users=db.query(UserLogin).all()
    return users


# Get_user_by_id 


@user_router.get("/user_by_id/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(connect_db)):
    user_by_id = db.query(UserLogin).filter(UserLogin.user_id == user_id).first()

    if not user_by_id:
        raise HTTPException(status_code=404, detail="User not found")

    return user_by_id


@user_router.put("/update/{user_id}")
def update_user(user_id: int, data: SignupSchema, db: Session = Depends(connect_db)):

    user = db.query(UserLogin).filter(UserLogin.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check username duplication
    if data.username != user.username:
        existing_user = db.query(UserLogin).filter(UserLogin.username == data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

    # Check email duplication
    if data.email != user.email:
        existing_email = db.query(UserLogin).filter(UserLogin.email == data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Update fields
    user.username = data.username
    user.email = data.email
    user.password = data.password
    user.phone = data.phone
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully!", "updated_user": user}


@user_router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(connect_db)):

    user = db.query(UserLogin).filter(UserLogin.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully!"}