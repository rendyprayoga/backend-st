from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.crud.product import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
    get_top_products,
    create_category_index
)
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.on_event("startup")
async def startup_event():
    await create_category_index()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(product: ProductCreate):
    created_product = await create_product(product)
    return ProductResponse(
        id=str(created_product.id), 
        name=created_product.name,
        description=created_product.description,
        price=created_product.price,
        category=created_product.category,
        stock=created_product.stock,
        status=created_product.status,
        image_url=created_product.image_url,
        created_at=created_product.created_at,
        updated_at=created_product.updated_at
    )

@router.get(
    "/", 
    response_model=List[ProductResponse],
    summary="Get All Products"
)
async def get_all_products():
    products = await get_products()
    return [
        ProductResponse(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
            status=product.status,
            image_url=product.image_url,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        for product in products
    ]

@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: str):
    product = await get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return ProductResponse(
        id=str(product.id), 
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        stock=product.stock,
        status=product.status,
        image_url=product.image_url,
        created_at=product.created_at,
        updated_at=product.updated_at
    )

@router.put(
    "/{product_id}", 
    response_model=ProductResponse,
    summary="Update Existing Product",
)
async def update_existing_product(product_id: str, product: ProductUpdate):
    updated_product = await update_product(product_id, product)
    
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return ProductResponse(
        id=str(updated_product.id),
        name=updated_product.name,
        description=updated_product.description,
        price=updated_product.price,
        category=updated_product.category,
        stock=updated_product.stock,
        status=updated_product.status,
        image_url=updated_product.image_url,
        created_at=updated_product.created_at,
        updated_at=updated_product.updated_at
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_product(product_id: str):
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return None