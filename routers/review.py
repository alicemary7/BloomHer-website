from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.review import Review
from models.product import Product
from schemas.review import ReviewCreate, ReviewOut

review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@review_router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(user_id: int = Query(...), data: ReviewCreate = None, db: Session = Depends(connect_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    review = Review(user_id=user_id, product_id=data.product_id, rating=data.rating, comment=data.comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@review_router.get("/product/{product_id}", response_model=List[ReviewOut])
def get_product_reviews(product_id: int, db: Session = Depends(connect_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()


@review_router.get("/user/{user_id}", response_model=List[ReviewOut])
def get_user_reviews(user_id: int, db: Session = Depends(connect_db)):
    return db.query(Review).filter(Review.user_id == user_id).all()


@review_router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, user_id: int = Query(...), db: Session = Depends(connect_db)):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return None
