from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.order import Order
from models.product import Product
from schemas.order import OrderCreate, OrderOut

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderOut)
def create_order(
    user_id: int,
    order_data: OrderCreate,
    db: Session = Depends(connect_db)
):
    """Create a new order for a single product"""
    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_amount = product.price * order_data.quantity

    order = Order(
        user_id=user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@order_router.get("/user/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(connect_db)):
    """Get all orders for a user"""
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


@order_router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(connect_db)):
    """Get order details with all items"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(connect_db)
):
    """Update order status (pending, shipped, delivered)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(connect_db)):
    """Delete an order and all its items"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message":"deleted successfully"}
