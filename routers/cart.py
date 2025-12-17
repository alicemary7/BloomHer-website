from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.cart import Cart
from schemas.cart import CartOut
from dependencies import connect_db

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.get("/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db: Session = Depends(connect_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart

@cart_router.delete("/{user_id}")
def clear_cart(user_id: int, db: Session = Depends(connect_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    db.delete(cart)
    db.commit()
    return {"message": "Cart cleared successfully"}

@cart_router.patch("/{user_id}/toggle-active")
def toggle_cart_active(user_id: int, db: Session = Depends(connect_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart.is_active = not cart.is_active
    db.commit()
    db.refresh(cart)
    return cart
