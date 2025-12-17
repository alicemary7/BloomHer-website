from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import connect_db
from models.product import Product, ProductVariant, ProductFeature
from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    VariantCreate,
    FeatureCreate,
    FeatureUpdate,
    VariantUpdate,
    VariantResponse,
    FeatureResponse
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(connect_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.post("/{product_id}/variants", response_model=dict)
def add_variants(
    product_id: int,
    variants: List[VariantCreate],
    db: Session = Depends(connect_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for variant in variants:
        db_variant = ProductVariant(
            product_id=product_id,
            size=variant.size,
            pads_count=variant.pads_count,
            stock=variant.stock,
            
        )
        db.add(db_variant)

    db.commit()
    return {"message": "Variants added successfully"}


@router.post("/{product_id}/features", response_model=dict)
def add_features(
    product_id: int,
    features: List[FeatureCreate],
    db: Session = Depends(connect_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for feature in features:
        db_feature = ProductFeature(
            product_id=product_id,
            feature_text=feature.feature_text
        )
        db.add(db_feature)

    db.commit()
    return {"message": "Features added successfully"}


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(connect_db)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_single_product(product_id: int, db: Session = Depends(connect_db)):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_active == True)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(connect_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}/deactivate", response_model=dict)
def deactivate_product(product_id: int, db: Session = Depends(connect_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active = False
    db.commit()
    return {"message": "Product deactivated successfully"}


@router.get("/{product_id}/variants", response_model=List[VariantResponse])
def get_product_variants(product_id: int, db: Session = Depends(connect_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    variants = db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()
    return variants


@router.get("/{product_id}/features", response_model=List[FeatureResponse])
def get_product_features(product_id: int, db: Session = Depends(connect_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    features = db.query(ProductFeature).filter(ProductFeature.product_id == product_id).all()
    return features


@router.put("/variants/{variant_id}", response_model=dict)
def update_variant(
    variant_id: int,
    data: VariantUpdate,
    db: Session = Depends(connect_db)
):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(variant, key, value)

    db.commit()
    db.refresh(variant)

    return {"message": "Variant updated successfully"}


@router.put("/features/{feature_id}", response_model=dict)
def update_feature(
    feature_id: int,
    data: FeatureUpdate,
    db: Session = Depends(connect_db)
):
    feature = db.query(ProductFeature).filter(ProductFeature.id == feature_id).first()

    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    if data.feature_text:
        feature.feature_text = data.feature_text
    db.commit()
    db.refresh(feature)

    return {"message": "Feature updated successfully"}


@router.delete("/variants/{variant_id}", response_model=dict)
def delete_variant(variant_id: int, db: Session = Depends(connect_db)):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    db.delete(variant)
    db.commit()

    return {"message": "Variant deleted successfully"}


@router.delete("/features/{feature_id}", response_model=dict)
def delete_feature(feature_id: int, db: Session = Depends(connect_db)):
    feature = db.query(ProductFeature).filter(ProductFeature.id == feature_id).first()

    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    db.delete(feature)
    db.commit()

    return {"message": "Feature deleted successfully"}










