from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.order import OrderItem, Order
from models.product import Product
from schemas.order_items import OrderItemCreate, OrderItemOut

order_items_router = APIRouter(prefix="/order-items", tags=["Order Items"])


@order_items_router.post("/{order_id}", response_model=OrderItemOut, status_code=status.HTTP_201_CREATED)
def add_item_to_order(
    order_id: int,
    item_data: OrderItemCreate,
    db: Session = Depends(connect_db)
):
    """Add an item to an order"""
    
    # Check if order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create order item
    order_item = OrderItem(
        order_id=order_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        price=product.price
    )
    
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    
    return order_item


@order_items_router.get("/{order_id}", response_model=List[OrderItemOut])
def get_order_items(order_id: int, db: Session = Depends(connect_db)):
    """Get all items in an order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return items


@order_items_router.get("/{order_id}/{item_id}", response_model=OrderItemOut)
def get_order_item(order_id: int, item_id: int, db: Session = Depends(connect_db)):
    """Get a specific item from an order"""
    
    item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == order_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@order_items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_order(item_id: int, db: Session = Depends(connect_db)):
    """Remove an item from an order"""
    
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return None
