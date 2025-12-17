from fastapi import FastAPI
from db.database import Base, engine
from models import (
    Product, ProductVariant, ProductFeature,
    User, Cart, CartItem, Review, Order, OrderItem
)
from routers.product import router
from routers.users import user_router
from routers.cart import cart_router
from routers.cart_items import cart_item_router
from routers.order import order_router
from routers.order_items import order_items_router
from routers.review import review_router

Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def greet():
    return {"message":"Welcome to server"}

app.include_router(router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(cart_item_router)
app.include_router(order_router)
app.include_router(order_items_router)
app.include_router(review_router)


