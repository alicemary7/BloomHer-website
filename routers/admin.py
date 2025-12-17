from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.admin import Admin
from models.users import User
from schemas.admin import AdminCreate, AdminOut

admin_router = APIRouter(prefix="/admins", tags=["Admins"])


@admin_router.post("/", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
def create_admin(data: AdminCreate, db: Session = Depends(connect_db)):
    # if user_id provided, ensure user exists
    if data.user_id:
        user = db.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    # check existing admin by email
    existing = db.query(Admin).filter(Admin.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    admin = Admin(user_id=data.user_id, email=data.email, password=data.password, is_super=data.is_super)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@admin_router.get("/", response_model=List[AdminOut])
def list_admins(db: Session = Depends(connect_db)):
    return db.query(Admin).all()


@admin_router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, db: Session = Depends(connect_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return None
