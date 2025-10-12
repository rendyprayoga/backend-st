from typing import List, Optional
from bson import ObjectId
from app.database import get_database
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud.activity_log import create_activity_log
from datetime import datetime

db = get_database()
products_collection = db["products"]

async def create_category_index():
    await products_collection.create_index("category")

async def create_product(product: ProductCreate) -> Product:
    product_dict = product.dict()
    new_product = Product(**product_dict)
    result = await products_collection.insert_one(new_product.dict(by_alias=True))
    
    # Log activity
    await create_activity_log(
        action="create",
        resource="product",
        resource_id=result.inserted_id,
        user_id=result.inserted_id,  
        details={"name": product.name}
    )
    
    created_product = await products_collection.find_one({"_id": result.inserted_id})
    return Product(**created_product)

async def get_products(skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Product]:
    query = {}
    if category:
        query["category"] = category
    
    products = await products_collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return [Product(**product) for product in products]

async def get_product(product_id: str) -> Optional[Product]:
    if ObjectId.is_valid(product_id):
        product = await products_collection.find_one({"_id": product_id})
        print(f"{product=}")
        if product:
            return Product(**product)
    return None


async def update_product(product_id: str, product: ProductUpdate) -> Optional[Product]:
        update_data = {k: v for k, v in product.dict(exclude_unset=True).items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()  
            
            result = await products_collection.update_one(
                {"_id":product_id}, 
                {"$set": update_data}
            )
            
            if result.modified_count == 1:
        
                await create_activity_log(
                    action="update",
                    resource="product",
                    resource_id=product_id,
                    user_id=product_id,  
                    details=update_data
                )
                
                updated_product = await products_collection.find_one({"_id": product_id})
                return Product(**updated_product)
        return None


async def delete_product(product_id: str) -> bool:
    if ObjectId.is_valid(product_id):
        product = await products_collection.find_one({"_id": product_id})
        
        result = await products_collection.delete_one({"_id": product_id})
        if result.deleted_count == 1:
            await create_activity_log(
                action="delete",
                resource="product",
                resource_id=product_id,
                user_id=product_id, 
                details={"name": product["name"]} if product else {}
            )
            return True
    return False

async def get_top_products(by: str = "price", limit: int = 5) -> List[Product]:
    if by == "price":
        sort_field = "price"
    elif by == "created_at":
        sort_field = "created_at"
    else:
        sort_field = "price"  
    
    products = await products_collection.find().sort(sort_field, -1).limit(limit).to_list(length=limit)
    return [Product(**product) for product in products]