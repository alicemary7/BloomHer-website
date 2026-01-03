from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from dependencies import connect_db
from models import Product
from schemas.product import ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(connect_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("/")
def get_products(db: Session = Depends(connect_db)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.put("/{product_id}")
def update_product(
    product_id: int, data: ProductCreate, db: Session = Depends(connect_db)
):
    update_product = db.query(Product).filter(Product.id == product_id).first()
    if not update_product:
        raise HTTPException(status_code=404, detail="product not found")
    update_product.name = data.name
    update_product.description = data.description
    update_product.price = data.price
    update_product.size = data.size
    update_product.pad_count = data.pad_count
    update_product.features = update_product.features
    update_product.stock = data.stock

    db.commit()
    db.refresh(update_product)

    return update_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(connect_db)):
    delete_product = db.query(Product).filter(Product.id == product_id).first()

    if not delete_product:
        raise HTTPException(status_code=404, detail="product not found")
    db.delete(delete_product)
    db.commit()
    return {"message": "deleted successfully"}
