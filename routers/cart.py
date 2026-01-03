from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.cart import Cart
from schemas.cart import CartOut, CartCreate
from dependencies import connect_db

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.get("/{user_id}", response_model=List[CartOut])
def get_cart(user_id: int, db: Session = Depends(connect_db)):
    # Return all cart items for the user
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return cart_items

@cart_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
def add_to_cart(user_id: int, cart_data: CartCreate, db: Session = Depends(connect_db)):
    # Check if item already exists for this user
    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id, 
        Cart.product_id == cart_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    new_cart_item = Cart(
        user_id=user_id,
        product_id=cart_data.product_id,
        quantity=cart_data.quantity
    )
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item

@cart_router.delete("/{user_id}")
def clear_cart(user_id: int, db: Session = Depends(connect_db)):
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared successfully"}

@cart_router.delete("/{user_id}/item/{product_id}")
def remove_cart_item(user_id: int, product_id: int, db: Session = Depends(connect_db)):
    item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}

