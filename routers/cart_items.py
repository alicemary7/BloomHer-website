from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.cart import Cart
from models.cart_items import CartItem
from models.product import Product
from schemas.cart_items import CartItemCreate, CartItemUpdate, CartItemOut
from dependencies import connect_db

cart_item_router = APIRouter(prefix="/cart-items", tags=["Cart Items"])

@cart_item_router.post("/{user_id}", response_model=CartItemOut)
def add_to_cart(
    user_id: int,
    data: CartItemCreate,
    db: Session = Depends(connect_db)
):
    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Get product to fetch price
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if item already in cart
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity,
            price=product.price
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return item

@cart_item_router.put("/{item_id}", response_model=CartItemOut)
def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    db: Session = Depends(connect_db)
):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item

@cart_item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(connect_db)
):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(item)
    db.commit()
    return None