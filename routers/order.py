from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate, OrderOut

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    user_id: int = Query(...),
    order_data: OrderCreate = None,
    db: Session = Depends(connect_db)
):
    """Create a new order with items"""
    if order_data is None:
        raise HTTPException(status_code=400, detail="order_data required in body")
    
    total_amount = 0
    order_items = []
    
    # Validate products and calculate total
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        item_total = product.price * item.quantity
        total_amount += item_total
        order_items.append((item.product_id, item.quantity, product.price))
    
    # Create order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return 'value added successfully'
    
    # Add order items
    for product_id, quantity, price in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    return order


@order_router.get("/user/{user_id}", response_model=List[OrderOut])
def get_user_orders(user_id: int, db: Session = Depends(connect_db)):
    """Get all orders for a user"""
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


@order_router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(connect_db)):
    """Get order details with all items"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    new_status: str = Query(...),
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
    return None
